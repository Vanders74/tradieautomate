#!/usr/bin/env python3
"""
GSC Auto-Index Requester for tradieautomate.com
================================================
Reads all URLs from the live sitemap and submits each for indexing
via the Google Search Console URL Inspection API.

Usage:
    # With service account JSON file:
    python scripts/gsc-index-requester.py --service-account path/to/service-account.json

    # With env var (recommended for CI/Netlify):
    GSC_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}' python scripts/gsc-index-requester.py

    # Dry run (no actual API calls):
    python scripts/gsc-index-requester.py --dry-run

Requirements:
    pip install google-auth google-auth-httplib2 requests

Setup (one-time):
    See SETUP section below or README for full instructions.

SETUP:
    1. Go to https://console.cloud.google.com/
    2. Create a project (or use existing)
    3. Enable "Google Search Console API" and "Web Search Indexing API"
    4. Create a Service Account:
       - IAM & Admin > Service Accounts > Create Service Account
       - Name: "gsc-index-requester"
       - Download JSON key → save as scripts/service-account.json (NEVER commit this)
    5. In Google Search Console (https://search.google.com/search-console/):
       - Open tradieautomate.com property
       - Settings > Users and permissions > Add user
       - Add the service account email (e.g. gsc-index-requester@your-project.iam.gserviceaccount.com)
       - Permission: Full
    6. Add JSON contents as NETLIFY env var: GSC_SERVICE_ACCOUNT_JSON
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

try:
    import google.oauth2.service_account as service_account_module
    import google.auth.transport.requests as google_requests
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install google-auth google-auth-httplib2 requests")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
SITE_URL = "https://tradieautomate.com"
SITEMAP_URL = f"{SITE_URL}/sitemap-0.xml"

# GSC URL Inspection API endpoint
INSPECTION_API_URL = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

# Google Indexing API (alternative — sends URL UPDATED signal)
INDEXING_API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# OAuth scopes needed
SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/indexing",
]

# Rate limiting — GSC API quota: 2,000 requests/day, ~1 req/sec safe
REQUEST_DELAY_SECONDS = 1.5


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_credentials(service_account_path: str | None = None):
    """Load Google service account credentials from file or env var."""
    sa_json = None

    # 1. Check env var first (for CI/Netlify)
    env_json = os.environ.get("GSC_SERVICE_ACCOUNT_JSON")
    if env_json:
        try:
            sa_json = json.loads(env_json)
            print("✓ Loaded credentials from GSC_SERVICE_ACCOUNT_JSON env var")
        except json.JSONDecodeError as e:
            print(f"ERROR: GSC_SERVICE_ACCOUNT_JSON is not valid JSON: {e}")
            sys.exit(1)

    # 2. Check file path
    if not sa_json and service_account_path:
        if not os.path.exists(service_account_path):
            print(f"ERROR: Service account file not found: {service_account_path}")
            sys.exit(1)
        with open(service_account_path) as f:
            sa_json = json.load(f)
        print(f"✓ Loaded credentials from {service_account_path}")

    # 3. Check default location
    if not sa_json:
        default_path = os.path.join(os.path.dirname(__file__), "service-account.json")
        if os.path.exists(default_path):
            with open(default_path) as f:
                sa_json = json.load(f)
            print(f"✓ Loaded credentials from {default_path}")

    if not sa_json:
        print(
            "\n❌ No credentials found!\n"
            "\nProvide credentials one of these ways:\n"
            "  1. Set env var: GSC_SERVICE_ACCOUNT_JSON='{...json...}'\n"
            "  2. Pass flag: --service-account path/to/service-account.json\n"
            "  3. Place file at: scripts/service-account.json\n"
            "\nSee script header for full setup instructions."
        )
        sys.exit(1)

    creds = service_account_module.Credentials.from_service_account_info(
        sa_json, scopes=SCOPES
    )
    return creds


def get_access_token(creds) -> str:
    """Get a fresh OAuth2 access token."""
    auth_request = google_requests.Request()
    creds.refresh(auth_request)
    return creds.token


def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    """Fetch and parse URLs from the sitemap."""
    print(f"📋 Fetching sitemap: {sitemap_url}")
    resp = requests.get(sitemap_url, timeout=30)
    resp.raise_for_status()

    import re
    urls = re.findall(r"<loc>(.*?)</loc>", resp.text)
    print(f"  Found {len(urls)} URLs in sitemap")
    return urls


def request_indexing_via_inspection_api(url: str, token: str) -> dict:
    """
    Request indexing using the GSC URL Inspection API.
    This is the standard GSC approach — it requests a crawl/index of the URL.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "inspectionUrl": url,
        "siteUrl": SITE_URL + "/",
        "languageCode": "en",
    }
    resp = requests.post(INSPECTION_API_URL, headers=headers, json=payload, timeout=30)
    return {"status_code": resp.status_code, "body": resp.json() if resp.content else {}}


def request_indexing_via_indexing_api(url: str, token: str) -> dict:
    """
    Submit URL_UPDATED notification via Google Indexing API.
    Faster for getting URLs crawled — originally for job postings but works broadly.
    Note: Site must be verified in GSC for the service account.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "url": url,
        "type": "URL_UPDATED",
    }
    resp = requests.post(INDEXING_API_URL, headers=headers, json=payload, timeout=30)
    return {"status_code": resp.status_code, "body": resp.json() if resp.content else {}}


def print_result(url: str, result: dict, method: str) -> bool:
    """Print result and return True if successful."""
    status = result["status_code"]
    body = result.get("body", {})

    if status == 200:
        print(f"  ✅ {url}")
        return True
    elif status == 403:
        print(f"  🔒 {url} — 403 Forbidden (check service account permissions in GSC)")
        return False
    elif status == 429:
        print(f"  ⏳ {url} — 429 Rate limited (slow down)")
        return False
    elif status == 400:
        error_msg = body.get("error", {}).get("message", "Bad request")
        print(f"  ⚠️  {url} — 400 Bad Request: {error_msg}")
        return False
    else:
        print(f"  ❌ {url} — {status}: {body}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Submit tradieautomate.com sitemap URLs for Google indexing"
    )
    parser.add_argument(
        "--service-account",
        help="Path to service account JSON file",
        default=None,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List URLs without making API calls",
    )
    parser.add_argument(
        "--method",
        choices=["inspection", "indexing", "both"],
        default="indexing",
        help="API method to use (default: indexing — faster for new URLs)",
    )
    parser.add_argument(
        "--url",
        help="Index a single URL instead of the full sitemap",
        default=None,
    )
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  GSC Auto-Index Requester — tradieautomate.com")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}\n")

    # Get URLs to process
    if args.url:
        urls = [args.url]
        print(f"🎯 Single URL mode: {args.url}\n")
    else:
        urls = fetch_sitemap_urls(SITEMAP_URL)
        print()

    if args.dry_run:
        print("🔍 DRY RUN — No API calls will be made\n")
        print("URLs that would be submitted:")
        for url in urls:
            print(f"  • {url}")
        print(f"\nTotal: {len(urls)} URLs")
        return

    # Load credentials
    creds = load_credentials(args.service_account)
    token = get_access_token(creds)
    print(f"✓ Authenticated as: {creds.service_account_email}\n")

    # Submit each URL
    success_count = 0
    fail_count = 0
    method = args.method

    print(f"🚀 Submitting {len(urls)} URLs via {method.upper()} API...\n")

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url.replace(SITE_URL, '')}")

        try:
            if method == "indexing" or method == "both":
                result = request_indexing_via_indexing_api(url, token)
                ok = print_result(url, result, "indexing")

            if method == "inspection" or method == "both":
                result = request_indexing_via_inspection_api(url, token)
                ok = print_result(url, result, "inspection")

            if ok:
                success_count += 1
            else:
                fail_count += 1

        except requests.RequestException as e:
            print(f"  ❌ Network error for {url}: {e}")
            fail_count += 1

        # Rate limiting
        if i < len(urls):
            time.sleep(REQUEST_DELAY_SECONDS)

    # Summary
    print(f"\n{'='*60}")
    print(f"  Results: {success_count} ✅  |  {fail_count} ❌")
    print(f"  Total URLs processed: {len(urls)}")
    print(f"{'='*60}")

    if fail_count > 0:
        print("\n⚠️  Some URLs failed. Common causes:")
        print("  • Service account not added to GSC property (most common)")
        print("  • Google Indexing API not enabled in Cloud Console")
        print("  • Service account email not matching GSC property owner")
        sys.exit(1)
    else:
        print("\n✅ All URLs submitted successfully!")


if __name__ == "__main__":
    main()
