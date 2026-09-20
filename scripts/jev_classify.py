#!/usr/bin/env python3
"""JEV classification wrapper for TradieAutomate.

Two backends:
1. OpenRouter — `POST /api/alpha/decisions`, model `~typesafe/jev-latest`
   ($0.042/MTok input, free output). Preferred: simplest, key-optional via env.
2. Vercel AI Gateway — legacy Node.js wrapper (free tier expired, kept as fallback).

Output contract (normalized so callers don't care which backend): for each question:
- choice  → {"type": "choice", "choice": ..., "probabilities": {...}}
- score   → {"type": "score", "score": N, "probabilities": [...]}  (OpenRouter score has criteria indices)
- boolean → {"type": "boolean", "choice": True/False, "noul": prob, "probabilities": {...}}
"""
import json
import os
import subprocess
import urllib.error
import urllib.request

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/alpha/decisions"
OPENROUTER_MODEL = "~typesafe/jev-latest"
JEV_SCRIPT = os.path.expanduser("/Users/shane/investments/scripts/jev-evaluate.mjs")


def _read_env(name):
    env_path = os.path.expanduser("~/.hermes/.env")
    try:
        for line in open(env_path):
            if line.startswith("#"):
                continue
            if name + "=" in line:
                return line.split("=", 1)[1].strip().strip("'\"")
    except FileNotFoundError:
        pass
    return os.environ.get(name, "")


def _normalize_openrouter(answers):
    """Map OpenRouter 'answers' to the wrapper's normalized output contract."""
    out = {}
    for name, raw in (answers or {}).items():
        q = dict(raw or {})
        qtype = q.get("type")
        if qtype == "noul":
            # probability 0..1 -> also derive a boolean choice for consistency
            prob = q.get("noul", q.get("probability", 0))
            out[name] = {
                "type": "boolean",
                "choice": bool(prob >= 0.5),
                "noul": round(float(prob), 4),
                "probabilities": {"true": round(float(prob), 4), "false": round(1 - float(prob), 4)},
            }
        elif qtype == "choice":
            out[name] = {
                "type": "choice",
                "choice": q.get("choice"),
                "probabilities": q.get("probabilities", {}),
            }
        elif qtype == "score":
            # OpenRouter score answer has criteria field with per-index probabilities
            probs = q.get("criteria") if isinstance(q.get("criteria"), dict) else {}
            out[name] = {
                "type": "score",
                "score": q.get("score"),
                "probabilities": probs,
            }
        else:
            out[name] = q
    return out


def jev_classify_openrouter(state_text, questions, timeout=30):
    """Call Jev via OpenRouter Decisions API. questions: {name: {type, instructions, criteria}}.
    type: 'choice' | 'score' | 'boolean' (converted to 'noul' for OpenRouter)."""
    key = _read_env("OPENROUTER_API_KEY")
    if not key:
        return {"_error": "No OPENROUTER_API_KEY found"}

    # Translate 'boolean' -> 'noul' for OpenRouter
    or_questions = {}
    for name, spec in questions.items():
        q = dict(spec)
        if q.get("type") == "boolean":
            q["type"] = "noul"
        or_questions[name] = q

    payload = {
        "model": OPENROUTER_MODEL,
        "state": state_text[:120000],
        "questions": or_questions,
    }
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "X-Title": "TradieAutomate",
    }
    req = urllib.request.Request(
        OPENROUTER_ENDPOINT, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        return {"_error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"_error": f"Request failed: {str(e)[:200]}"}

    answers = resp.get("answers") or resp.get("data", {}).get("answers")
    if answers is None:
        return {"_error": f"Unexpected response shape: {json.dumps(resp)[:300]}"}
    return _normalize_openrouter(answers)


def jev_classify_openrouter_legacy(state_text, questions, timeout=30):
    """Legacy path: Vercel AI Gateway thru the Node.js wrapper."""
    key = _read_env("VERCEL_AI_GATEWAY_KEY")
    if not key:
        return {"_error": "No VERCEL_AI_GATEWAY_KEY found"}
    env = os.environ.copy()
    env["VERCEL_AI_GATEWAY_KEY"] = key
    cmd = ["node", JEV_SCRIPT, "typesafe-ai/jev", state_text[:120000]]
    for name, spec in questions.items():
        cmd.append(json.dumps({name: spec}))
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout, env=env, text=True)
    except FileNotFoundError:
        return {"_error": f"Node.js not found or script missing at {JEV_SCRIPT}"}
    except subprocess.TimeoutExpired:
        return {"_error": "JEV call timed out"}
    if r.returncode != 0:
        err = r.stderr.strip()
        if err.startswith("{"):
            return json.loads(err)
        return {"_error": err[:300]}
    try:
        return json.loads(r.stdout.strip())
    except json.JSONDecodeError:
        return {"_error": f"Invalid JSON response: {r.stdout.strip()[:200]}"}


def jev_classify(state_text, questions, model=None, timeout=30):
    """Preferred entrypoint: OpenRouter first, legacy Vercel fallback."""
    err = None
    # OpenRouter needs a key; if absent fall through to legacy
    if _read_env("OPENROUTER_API_KEY"):
        res = jev_classify_openrouter(state_text, questions, timeout=timeout)
        if "_error" not in res:
            return res
        err = res["_error"]
    # Legacy fallback (Vercel gateway)
    res = jev_classify_openrouter_legacy(state_text, questions, timeout=timeout)
    if "_error" not in res:
        return res
    # Return whichever error is more relevant (mention both if both failed)
    return {"_error": (err + " | " if err else "") + res["_error"]}


if __name__ == "__main__":
    res = jev_classify(
        "A CCEW is required for notifiable electrical work in NSW within 7 days.",
        {"intent": {"type": "choice", "instructions": "Search intent",
                    "criteria": {"lookup": "Looking for data",
                                 "compliance": "Legal requirement",
                                 "comparison": "Comparing options"}},
         "stakes": {"type": "boolean", "instructions": "Has a deadline?"}},
    )
    print(json.dumps(res, indent=2))