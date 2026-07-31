#!/usr/bin/env python3
"""Extract cron job status for the dashboard generator."""
import json
import os
import re
import subprocess
from datetime import datetime

HERMES_BIN = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/hermes")
OUTPUT_FILE = os.path.expanduser("~/tradieautomate/cron_status.json")


def parse_cron_output(text: str) -> list[dict]:
    """Parse `hermes cron list` output into structured data."""
    jobs = []
    current_job = None

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Match job header: "  job_id [active]" or "  job_id [paused]"
        m = re.match(r"^([a-f0-9]+)\s+\[(\w+)\]", line)
        if m:
            if current_job:
                jobs.append(current_job)
            current_job = {
                "id": m.group(1),
                "state": m.group(2),
                "name": "",
                "schedule": "",
                "last_run": None,
                "last_status": None,
                "last_error": None,
                "next_run": None,
            }
            continue

        if not current_job:
            continue

        if line.startswith("Name:"):
            current_job["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("Schedule:"):
            current_job["schedule"] = line.split(":", 1)[1].strip()
        elif line.startswith("Next run:"):
            current_job["next_run"] = line.split(":", 1)[1].strip()
        elif line.startswith("Last run:"):
            parts = line.split(":", 1)[1].strip()
            # Split timestamp and status
            m2 = re.match(r"^(.+?)\s+(ok|error):?\s*(.*)", parts)
            if m2:
                current_job["last_run"] = m2.group(1).strip()
                current_job["last_status"] = m2.group(2).strip()
                current_job["last_error"] = m2.group(3).strip()[:120] if m2.group(3) else None

    if current_job:
        jobs.append(current_job)

    return jobs


def main():
    try:
        result = subprocess.run(
            [HERMES_BIN, "cron", "list"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            raise RuntimeError(f"hermes cron list exited {result.returncode}")

        jobs = parse_cron_output(result.stdout)

        data = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": len(jobs),
            "ok": sum(1 for j in jobs if j["last_status"] == "ok"),
            "error": sum(1 for j in jobs if j["last_status"] == "error"),
            "never_run": sum(1 for j in jobs if j["last_status"] is None),
            "paused": sum(1 for j in jobs if j["state"] == "paused"),
            "jobs": jobs,
        }

        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(data, f, indent=2)

        # Silent on success (watchdog pattern for dashboard wrapper)
        return 0

    except Exception as e:
        # Write error state so dashboard can show "unavailable"
        error_data = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": 0,
            "ok": 0,
            "error": 0,
            "never_run": 0,
            "paused": 0,
            "jobs": [],
            "_error": str(e)[:200],
        }
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(error_data, f, indent=2)
        return 1


if __name__ == "__main__":
    exit(main())
