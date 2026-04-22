# Scripts

Utility scripts for tradieautomate.com site management.

## gsc-index-requester.py

Submits all URLs from the live sitemap to Google for indexing via the Google Search Console API.

### Requirements

```bash
pip install google-auth google-auth-httplib2 requests
```

### Setup (one-time)

**Step 1: Create Google Cloud project and enable APIs**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g. "tradieautomate-gsc")
3. Enable both APIs:
   - [Web Search Indexing API](https://console.cloud.google.com/apis/library/indexing.googleapis.com)
   - [Google Search Console API](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com)

**Step 2: Create a Service Account**

1. Go to IAM & Admin → Service Accounts → Create Service Account
2. Name: `gsc-index-requester`
3. Skip role assignments (permissions come from GSC)
4. Click the service account → Keys → Add Key → Create new key → JSON
5. Download the JSON file

**Step 3: Add service account to Google Search Console**

1. Go to [Google Search Console](https://search.google.com/search-console/)
2. Open the `tradieautomate.com` property
3. Settings → Users and permissions → Add user
4. Add the service account email (shown in the JSON as `client_email`)
5. Set permission to **Full**

**Step 4: Set environment variable (for Netlify/CI)**

In Netlify dashboard → Site settings → Environment variables:
```
GSC_SERVICE_ACCOUNT_JSON = {entire contents of the JSON key file}
```

### Usage

```bash
# Index all sitemap URLs (using env var or scripts/service-account.json)
python scripts/gsc-index-requester.py

# Specify service account file directly
python scripts/gsc-index-requester.py --service-account ~/my-service-account.json

# Index a single URL
python scripts/gsc-index-requester.py --url https://tradieautomate.com/blog/servicem8-review-2026/

# Dry run (no API calls, just list URLs)
python scripts/gsc-index-requester.py --dry-run
```

### Netlify Deploy Hook Integration

Add to `netlify.toml` to auto-index on every deploy:

```toml
[[plugins]]
  package = "@netlify/plugin-postbuild-commands"
  [plugins.inputs]
    commands = ["pip install google-auth google-auth-httplib2 requests && python scripts/gsc-index-requester.py"]
```

Or create a Netlify function that triggers on `deploy-succeeded` event.
