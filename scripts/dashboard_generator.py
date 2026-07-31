#!/usr/bin/env python3
"""
TradieAutomate Dashboard Generator

Pulls GSC + GA4 + content analysis, writes:
  - ~/tradieautomate/dashboard.json   (machine-readable, for cron agent)
  - ~/tradieautomate/dashboard.html   (human-readable, dark-themed single page)

Usage:
  cd ~/tradieautomate && source gvenv/bin/activate && unset PYTHONPATH
  python3 scripts/dashboard_generator.py

Config is loaded from scripts/ relative to this file, or overridden by env vars.
"""
import json
import os
import sys
import warnings
from datetime import date, datetime, timedelta
from pathlib import Path

warnings.filterwarnings("ignore")

# ── Config ──────────────────────────────────────────────────────────────────
SITE_URL = "https://tradieautomate.com/"
GA4_PROPERTY_ID = "536080845"
KEY_PATH = os.path.expanduser("~/tradieautomate/credentials/gsc_ga4_service_account.json")
CONTENT_DIR = os.path.expanduser("~/tradieautomate/repo/src/content/blog")
DASHBOARD_JSON = os.path.expanduser("~/tradieautomate/dashboard.json")
DASHBOARD_HTML = os.path.expanduser("~/tradieautomate/dashboard.html")
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

# ── GSC Helpers ─────────────────────────────────────────────────────────────

def _gsc_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(
        KEY_PATH, scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    return build("searchconsole", "v1", credentials=creds)

def _pull_gsc(service, site_url, start, end, dimensions):
    req = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": dimensions,
        "rowLimit": 5000,
    }
    resp = service.searchanalytics().query(siteUrl=site_url, body=req).execute()
    return resp.get("rows", [])

def pull_gsc_data():
    """Return {page_rows, query_rows, trend_windows, totals}."""
    svc = _gsc_service()
    today = date.today()
    end = today - timedelta(days=3)

    # Page-level: last 28 days
    page_rows = _pull_gsc(svc, SITE_URL, end - timedelta(days=27), end, ["page"])
    page_rows.sort(key=lambda r: -r["impressions"])

    # Query-level: last 28 days
    query_rows = _pull_gsc(svc, SITE_URL, end - timedelta(days=27), end, ["query"])
    query_rows.sort(key=lambda r: -r["impressions"])

    # Per-page query mapping: page+query dimensions, group by slug, top 5 per page
    pq_rows = _pull_gsc(svc, SITE_URL, end - timedelta(days=27), end, ["page", "query"])
    page_queries = {}  # slug -> [query dicts]
    for r in pq_rows:
        slug = r["keys"][0].replace(SITE_URL, "").strip("/").split("/")[-1] or "index"
        page_queries.setdefault(slug, []).append({
            "query": r["keys"][1],
            "clicks": r["clicks"],
            "impressions": r["impressions"],
            "ctr": round(r["ctr"] * 100, 2),
            "position": round(r["position"], 1),
        })
    for slug in page_queries:
        page_queries[slug].sort(key=lambda q: -q["impressions"])
        page_queries[slug] = page_queries[slug][:5]  # top 5

    # 3-month trend (3 x 28-day windows)
    trend_windows = []
    prior_page_data = {}  # slug -> {clicks, impressions, ctr, position} from Window 1
    for i in range(3):
        w_end = end - timedelta(days=28 * i)
        w_start = w_end - timedelta(days=27)
        rows = _pull_gsc(svc, SITE_URL, w_start, w_end, ["page"])
        clicks = sum(r["clicks"] for r in rows)
        impr = sum(r["impressions"] for r in rows)
        avg_pos = sum(r["position"] * r["impressions"] for r in rows) / max(impr, 1)
        pages_with_data = len(rows)
        trend_windows.append({
            "start": w_start.isoformat(),
            "end": w_end.isoformat(),
            "clicks": clicks,
            "impressions": impr,
            "avg_position": round(avg_pos, 1),
            "pages_with_data": pages_with_data,
        })
        # Capture per-page metrics from Window 1 (prior 28-day) for trend comparison
        if i == 1:
            for r in rows:
                slug = r["keys"][0].replace(SITE_URL, "").strip("/").split("/")[-1] or "index"
                prior_page_data[slug] = {
                    "prev_clicks": r["clicks"],
                    "prev_impressions": r["impressions"],
                    "prev_ctr": round(r["ctr"] * 100, 2),
                    "prev_position": round(r["position"], 1),
                }

    # Totals from last window
    totals = {
        "clicks": trend_windows[0]["clicks"] if trend_windows else 0,
        "impressions": trend_windows[0]["impressions"] if trend_windows else 0,
        "ctr": round((trend_windows[0]["clicks"] / max(trend_windows[0]["impressions"], 1)) * 100, 2) if trend_windows else 0,
        "avg_position": trend_windows[0]["avg_position"] if trend_windows else 0,
        "pages_with_data": trend_windows[0]["pages_with_data"] if trend_windows else 0,
    }

    # Clean page rows for JSON — deduplicate by slug (GSC sometimes splits trailing-slash variants)
    # Expected CTR by position (industry benchmarks)
    def _expected_ctr(pos):
        if pos <= 3: return 15.0
        if pos <= 5: return 8.0
        if pos <= 10: return 5.0
        if pos <= 15: return 3.0
        if pos <= 20: return 2.0
        if pos <= 30: return 1.0
        return 0.5

    pages = []
    seen = {}
    for r in page_rows:
        slug = r["keys"][0].replace(SITE_URL, "").strip("/").split("/")[-1] or "index"
        url = r["keys"][0]
        if slug in seen:
            seen[slug]["impressions"] += r["impressions"]
            seen[slug]["clicks"] += r["clicks"]
            # Recalc CTR from combined totals
            seen[slug]["ctr"] = round((seen[slug]["clicks"] / max(seen[slug]["impressions"], 1)) * 100, 2)
            seen[slug]["position"] = round(
                (seen[slug]["position"] * seen[slug]["_pos_impr"] + r["position"] * r["impressions"])
                / max(seen[slug]["_pos_impr"] + r["impressions"], 1), 1
            )
            seen[slug]["_pos_impr"] += r["impressions"]
            # Keep the URL with more impressions as primary
            if r["impressions"] > seen[slug].get("_max_impr", 0):
                seen[slug]["url"] = url
                seen[slug]["_max_impr"] = r["impressions"]
        else:
            seen[slug] = {
                "slug": slug,
                "url": url,
                "clicks": r["clicks"],
                "impressions": r["impressions"],
                "ctr": round(r["ctr"] * 100, 2),
                "position": round(r["position"], 1),
                "_max_impr": r["impressions"],
                "_pos_impr": r["impressions"],
            }

    for slug, v in seen.items():
        v.pop("_max_impr", None)
        v.pop("_pos_impr", None)
        # Pre-computed CTR gap
        v["expected_ctr"] = _expected_ctr(v["position"])
        v["ctr_ratio"] = round(v["ctr"] / max(v["expected_ctr"], 0.01), 2)
        # Merge prior-period metrics (from Window 1 trend data)
        prior = prior_page_data.get(slug)
        if prior:
            v["prev_clicks"] = prior["prev_clicks"]
            v["prev_impressions"] = prior["prev_impressions"]
            v["prev_ctr"] = prior["prev_ctr"]
            v["prev_position"] = prior["prev_position"]
        # Merge per-page top queries
        v["top_queries"] = page_queries.get(slug, [])
        pages.append(v)
    pages.sort(key=lambda p: -p["impressions"])

    # Top queries
    queries = []
    for r in query_rows[:30]:
        queries.append({
            "query": r["keys"][0],
            "clicks": r["clicks"],
            "impressions": r["impressions"],
            "ctr": round(r["ctr"] * 100, 2),
            "position": round(r["position"], 1),
        })

    return {
        "pages": pages,
        "queries": queries,
        "trend_windows": trend_windows,
        "totals": totals,
    }


# ── GA4 Helpers ─────────────────────────────────────────────────────────────

def _ga4_client():
    from google.oauth2 import service_account
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    creds = service_account.Credentials.from_service_account_file(
        KEY_PATH, scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    return BetaAnalyticsDataClient(credentials=creds)

def pull_ga4_data():
    """Return {totals, top_pages, channels}."""
    from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric

    client = _ga4_client()
    prop = f"properties/{GA4_PROPERTY_ID}"

    # Totals: last 28d vs prior 28d
    req = RunReportRequest(
        property=prop,
        metrics=[Metric(name="sessions"), Metric(name="totalUsers"),
                 Metric(name="engagementRate"), Metric(name="conversions")],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="today"),
                     DateRange(start_date="56daysAgo", end_date="29daysAgo")],
    )
    resp = client.run_report(req)
    totals = {"current": {}, "prior": {}}
    labels = ["current", "prior"]
    for i, row in enumerate(resp.rows):
        vals = [mv.value for mv in row.metric_values]
        totals[labels[i]] = {
            "sessions": int(vals[0]),
            "users": int(vals[1]),
            "engagement_rate": round(float(vals[2]), 3),
            "conversions": int(vals[3]),
        }

    # Tracking gap check
    conversions_all_zero = all(
        int(row.metric_values[3].value) == 0 for row in resp.rows
    )
    tracking_gap = conversions_all_zero

    # Top pages
    req2 = RunReportRequest(
        property=prop,
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="sessions"), Metric(name="engagedSessions"),
                 Metric(name="averageSessionDuration")],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="today")],
        limit=30,
        order_bys=[{"metric": {"metric_name": "sessions"}, "desc": True}],
    )
    resp2 = client.run_report(req2)
    top_pages = []
    for row in resp2.rows:
        path = row.dimension_values[0].value
        sess, eng, dur = (mv.value for mv in row.metric_values)
        top_pages.append({
            "path": path,
            "sessions": int(sess),
            "engaged_sessions": int(eng),
            "avg_duration_sec": int(float(dur)),
        })

    # Traffic sources
    req3 = RunReportRequest(
        property=prop,
        dimensions=[Dimension(name="sessionDefaultChannelGroup")],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="today")],
        order_bys=[{"metric": {"metric_name": "sessions"}, "desc": True}],
    )
    resp3 = client.run_report(req3)
    channels = {}
    for row in resp3.rows:
        channels[row.dimension_values[0].value] = int(row.metric_values[0].value)

    total_sessions = sum(channels.values())
    channel_list = [
        {"name": k, "sessions": v, "share": round(v / max(total_sessions, 1) * 100, 1)}
        for k, v in sorted(channels.items(), key=lambda x: -x[1])
    ]

    return {
        "totals": totals,
        "tracking_gap": tracking_gap,
        "top_pages": top_pages,
        "channels": channel_list,
        "total_sessions": total_sessions,
    }


def pull_ga4_conversions():
    """Return per-event conversion counts for the last 28 days."""
    from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric

    client = _ga4_client()
    prop = f"properties/{GA4_PROPERTY_ID}"

    req = RunReportRequest(
        property=prop,
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="today")],
        order_bys=[{"metric": {"metric_name": "eventCount"}, "desc": True}],
        limit=20,
    )
    resp = client.run_report(req)

    events = {}
    for row in resp.rows:
        name = row.dimension_values[0].value
        count = int(row.metric_values[0].value)
        events[name] = count

    # Extract our tracked conversion events
    conversions = {
        "affiliate_click": events.get("affiliate_click", 0),
        "trial_click": events.get("trial_click_1", 0),
        "lead_magnet_download": events.get("lead_magnet_download", 0),
        "playbook_signup": events.get("playbook_signup", 0),
    }
    conversions["total"] = sum(conversions.values())

    # Conversion rate: total conversions / total sessions
    return conversions


# ── Cron Status ─────────────────────────────────────────────────────────────

CRON_STATUS_JSON = os.path.expanduser("~/tradieautomate/cron_status.json")

def pull_cron_status():
    """Return cron job health summary. Reads from cron_status.py output."""
    if not os.path.exists(CRON_STATUS_JSON):
        return {"available": False, "error": "cron_status.json not found"}
    try:
        with open(CRON_STATUS_JSON) as f:
            data = json.load(f)
        data["available"] = True
        return data
    except Exception as e:
        return {"available": False, "error": str(e)[:200]}


# ── Content Analysis ────────────────────────────────────────────────────────

def analyze_content():
    """Return {posts, clusters, last_updated}."""
    if not os.path.isdir(CONTENT_DIR):
        return {"posts": [], "total": 0, "by_cluster": {}, "last_updated": None}

    posts = []
    cluster_keywords = {
        "servicem8": "ServiceM8 Reviews & Comparisons",
        "solar": "Solar Compliance & Installer Guides",
        "battery": "Battery & BESS",
        "ev": "EV Charging",
        "compliance": "Compliance & Safety",
        "electrical": "Electrical Licensing & Awards",
        "trade": "Trade Business Operations",
        "xero": "Trade Business Operations",
        "payroll": "Trade Business Operations",
        "simpro": "ServiceM8 Reviews & Comparisons",
        "tradify": "ServiceM8 Reviews & Comparisons",
        "fergus": "ServiceM8 Reviews & Comparisons",
        "aroflo": "ServiceM8 Reviews & Comparisons",
        "jobber": "ServiceM8 Reviews & Comparisons",
        "plumbers": "Trade Business Operations",
        "roofing": "Trade Business Operations",
        "painters": "Trade Business Operations",
        "tap-to-pay": "Trade Business Operations",
        "sms": "Trade Business Operations",
        "monitoring": "Solar Compliance & Installer Guides",
        "playbook": "Solar Compliance & Installer Guides",
        "vic-solar": "Solar Compliance & Installer Guides",
        "wa-electrical": "Electrical Licensing & Awards",
        "staying-compliant": "Compliance & Safety",
        "retrofit": "Battery & BESS",
        "stc-claim": "Solar Compliance & Installer Guides",
    }

    by_cluster = {}
    most_recent = None

    for f in sorted(Path(CONTENT_DIR).glob("*.md")):
        stat = f.stat()
        slug = f.stem
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")

        # Determine cluster
        cluster = "General"
        for key, name in cluster_keywords.items():
            if key in slug.lower():
                cluster = name
                break

        by_cluster.setdefault(cluster, 0)
        by_cluster[cluster] += 1

        if most_recent is None or mtime > most_recent:
            most_recent = mtime

        posts.append({"slug": slug, "mtime": mtime, "cluster": cluster})

    return {
        "posts": posts,
        "total": len(posts),
        "by_cluster": by_cluster,
        "last_updated": most_recent,
    }


# ── Delta / Anomaly Detection ───────────────────────────────────────────────

def compute_deltas(today_data, yesterday_data):
    """Compare today's data to yesterday's. Return delta dict + anomalies list."""
    deltas = {
        "gsc_clicks": today_data["gsc"]["totals"]["clicks"] - yesterday_data.get("gsc", {}).get("totals", {}).get("clicks", 0) if yesterday_data else 0,
        "gsc_impressions": today_data["gsc"]["totals"]["impressions"] - yesterday_data.get("gsc", {}).get("totals", {}).get("impressions", 0) if yesterday_data else 0,
        "gsc_ctr": round(today_data["gsc"]["totals"]["ctr"] - yesterday_data.get("gsc", {}).get("totals", {}).get("ctr", 0), 2) if yesterday_data else 0,
        "ga4_sessions": today_data["ga4"]["totals"]["current"]["sessions"] - yesterday_data.get("ga4", {}).get("totals", {}).get("current", {}).get("sessions", 0) if yesterday_data else 0,
        "page_movements": [],
    }

    anomalies = []
    today_pages = {p["slug"]: p for p in today_data["gsc"]["pages"]}

    # Always-on anomalies: zero-click pages (data issue, not comparison issue)
    for slug, tp in today_pages.items():
        if tp["impressions"] >= 500 and tp["clicks"] == 0:
            anomalies.append({
                "type": "zero_click",
                "severity": "high",
                "slug": slug,
                "detail": f"{tp['impressions']:,} impressions, zero clicks. Position {tp['position']}.",
                "action": f"Meta description rewrite is highest priority. Page has visibility but zero capture at position {tp['position']}.",
            })

    # Comparison-based deltas and anomalies (require yesterday's data)
    if yesterday_data:
        yesterday_pages = {p["slug"]: p for p in yesterday_data.get("gsc", {}).get("pages", [])}

        for slug, tp in today_pages.items():
            yp = yesterday_pages.get(slug)
            if yp:
                pos_change = round(yp["position"] - tp["position"], 1)  # positive = improved
                impr_change = tp["impressions"] - yp["impressions"]
                ctr_change = round(tp["ctr"] - yp["ctr"], 2)

                if abs(pos_change) >= 1 or abs(impr_change) >= 50 or abs(ctr_change) >= 0.2:
                    deltas["page_movements"].append({
                        "slug": slug,
                        "pos_change": pos_change,
                        "impr_change": impr_change,
                        "ctr_change": ctr_change,
                        "current_pos": tp["position"],
                        "current_ctr": tp["ctr"],
                        "current_impressions": tp["impressions"],
                    })

                # Anomalies: dropped positions
                if pos_change < -3:
                    anomalies.append({
                        "type": "position_drop",
                        "severity": "high",
                        "slug": slug,
                        "detail": f"Dropped {abs(pos_change)} positions to {tp['position']}. Was {yp['position']}.",
                        "action": f"Review content freshness and backlinks for {slug}. Consider updating publish date and adding recent regulatory references.",
                    })

                # Anomalies: CTR cliffs
                if ctr_change < -0.3 and abs(pos_change) < 1:
                    anomalies.append({
                        "type": "ctr_cliff",
                        "severity": "medium",
                        "slug": slug,
                        "detail": f"CTR dropped {abs(ctr_change)}% to {tp['ctr']}% with position unchanged. Someone wrote a better meta description.",
                        "action": f"Rewrite meta description for {slug}. Check SERP for competing snippets.",
                    })

        # Anomalies: new top-20 queries
        yesterday_queries = {q["query"]: q for q in yesterday_data.get("gsc", {}).get("queries", [])}
        for tq in today_data["gsc"]["queries"][:20]:
            if tq["query"] not in yesterday_queries and tq["position"] <= 20:
                anomalies.append({
                    "type": "new_query",
                    "severity": "low",
                    "slug": tq["query"],
                    "detail": f"New query entering top 20: '{tq['query']}' at position {tq['position']}.",
                    "action": f"Double down on '{tq['query']}' — create dedicated content or expand existing page.",
                })

    # Sort anomalies by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    anomalies.sort(key=lambda a: severity_order.get(a["severity"], 99))

    deltas["page_movements"].sort(key=lambda m: -abs(m["impr_change"]))
    return deltas, anomalies


# ── Insights Computation ────────────────────────────────────────────────────

# ── SEO Scoring Functions ──────────────────────────────────────────────────

def _score_article(slug):
    """Score a single article against the 7-pillar rubric. Returns dict or None."""
    md_path = os.path.join(CONTENT_DIR, f"{slug}.md")
    if not os.path.exists(md_path):
        return None
    
    try:
        with open(md_path) as f:
            content = f.read()
    except Exception:
        return None
    
    scores = {}
    
    # Split frontmatter and body
    if content.startswith('---'):
        end = content.find('---', 3)
        fm_text = content[3:end] if end > 0 else ''
        body = content[end+3:].strip() if end > 0 else content
    else:
        fm_text = ''
        body = content
    
    # Parse frontmatter (simple YAML subset — avoids PyYAML dependency)
    fm = {}
    if fm_text:
        import re as _re
        for line in fm_text.split('\n'):
            m = _re.match(r'^(\w+):\s*(.+)', line)
            if m:
                fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
        # Check for faq: array (multi-line)
        faq_section = _re.search(r'faq:\s*\n((?:\s+-.+\n?)+)', fm_text)
        if faq_section:
            fm['_faq_count'] = len(_re.findall(r'^\s+- question:', faq_section.group(1), _re.MULTILINE))
    
    import re as _re
    
    # === Pillar 1: Synthesis Density (20 pts) ===
    source_types = set()
    if _re.search(r'AS/NZS\s+\d+', body): source_types.add('standards')
    if _re.search(r'\.gov\.au', body): source_types.add('government')
    regs = ['Fair Work', 'Clean Energy Regulator', 'SafeWork', 'Energy Safe',
            'QBCC', 'Fair Trading', 'Building and Energy', 'Electrical Safety Office',
            'Clean Energy Council', 'Solar Accreditation Australia']
    if any(r.lower() in body.lower() for r in regs): source_types.add('regulatory')
    tools = ['Xero', 'ServiceM8', 'MYOB', 'simPRO', 'Tradify', 'AroFlo', 'Fergus']
    if any(t.lower() in body.lower() for t in tools): source_types.add('tools')
    if len(_re.findall(r'\$\d[\d,]+', body)) >= 2: source_types.add('costing')
    scores['synthesis'] = min(20, 7 * len(source_types))
    
    # === Pillar 2: AEO Readiness (20 pts) ===
    aeo = 0
    if fm.get('_faq_count', 0) >= 2: aeo += 7
    qa_pattern = _re.findall(r'^###\s+(?:What|How|Does|Can|Is|Do|Are|Should|When|Where|Why)\s', body, _re.MULTILINE)
    if len(qa_pattern) >= 2: aeo += 7
    words_300 = ' '.join(body.split()[:300])
    sents = _re.split(r'(?<=[.!?])\s+', words_300)
    for sent in sents[:5]:
        wc = len(sent.split())
        if 10 <= wc <= 60:
            if _re.search(r'\$\d|AS/NZS|is\s+a\s+', sent) or any(r.lower() in sent.lower() for r in regs):
                aeo += 6
                break
    scores['aeo'] = min(20, aeo)
    
    # === Pillar 3: Regulatory Precision (20 pts) ===
    reg_pairs = set()
    body_parts = _re.split(r'(?<=[.!?])\s+', body)
    for i, sent in enumerate(body_parts):
        ctx = ' '.join(body_parts[max(0,i-1):min(len(body_parts),i+2)])
        found = [r for r in regs if r.lower() in ctx.lower()]
        if found and (_re.search(r'Home Building Act|Electricity Safety Act|Electrical Safety Act|Fair Work Act|AS/NZS\s+\d+|Clause\s+\d+|Section\s+\d+|\.gov\.au|\$\d[\d,]+', ctx)):
            for r in found: reg_pairs.add(r)
    scores['regulatory'] = min(20, 7 * len(reg_pairs))
    
    # === Pillar 4: Formatting (12 pts) ===
    fmt = 0
    h_count = len(_re.findall(r'^##\s', body, _re.MULTILINE)) + len(_re.findall(r'^###\s', body, _re.MULTILINE))
    fmt += 4 if h_count >= 3 else (2 if h_count >= 1 else 0)
    paras = [p for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#') and not p.strip().startswith('```') and not p.strip().startswith('|')]
    max_w = max((len(p.split()) for p in paras), default=0)
    if any(len(p.split()) > 200 for p in paras): fmt -= 2
    elif max_w > 120: fmt -= 1
    bold = len(_re.findall(r'\*\*[^*]+\*\*', body))
    fmt += 2 if bold >= 3 else (1 if bold >= 1 else 0)
    bullets = len(_re.findall(r'^[-*]\s+.+(\n^[-*]\s+.+)+', body, _re.MULTILINE))
    fmt += 2 if bullets >= 2 else (1 if bullets >= 1 else 0)
    scores['formatting'] = max(0, min(12, fmt))
    
    # === Pillar 5: Technical SEO (8 pts) ===
    seo = 0
    slug_parts = slug.replace('-', ' ').lower().split()
    title_text = (fm.get('title', '') or '').lower()
    if any(p in slug for p in slug_parts[:3]): seo += 1
    if any(p in title_text for p in slug_parts[:3]): seo += 1
    first_100 = ' '.join(body.split()[:100]).lower()
    if any(p in first_100 for p in slug_parts[:3]): seo += 1
    h2s = _re.findall(r'^##\s+(.+)', body, _re.MULTILINE)
    if any(any(p in h2.lower() for p in slug_parts[:3]) for h2 in h2s): seo += 1
    desc = fm.get('description', '')
    dl = len(desc)
    seo += 3 if 120 <= dl <= 160 else (1 if dl > 0 else 0)
    if _re.search(r'\$\d|penalty|fine|deadline|audit', desc, _re.IGNORECASE): seo += 1
    scores['technical_seo'] = min(8, seo)
    
    # === Pillar 6: Internal Links (10 pts) ===
    out_links = len(set(_re.findall(r'\[([^\]]*)\]\(/blog/([^)\s]+)\)', body)))
    in_links = 0
    if os.path.isdir(CONTENT_DIR):
        import glob
        for mf in glob.glob(os.path.join(CONTENT_DIR, '*.md')):
            fslug = os.path.splitext(os.path.basename(mf))[0]
            if fslug == slug: continue
            try:
                fc = open(mf).read()
                if f'/blog/{slug}' in fc or f'/blog/{slug}/' in fc:
                    in_links += 1
            except: pass
    scores['internal_links'] = min(5, out_links) + min(5, in_links)
    
    # === Pillar 7: Freshness (10 pts) ===
    fresh = 0
    if fm.get('updatedDate'): fresh += 4
    years = set(_re.findall(r'\b(202[4-9]|2030)\b', body))
    fresh += 2 if len(years) >= 3 else (1 if len(years) >= 1 else 0)
    h2_sections = _re.split(r'^## ', body, flags=_re.MULTILINE)
    iso = sum(1 for s in h2_sections if _re.search(r'\$\d[\d,]+', s) and _re.search(r'\b(202[4-9]|2030)\b', s))
    fresh += 4 if iso >= 2 else (2 if iso >= 1 else 0)
    scores['freshness'] = min(10, fresh)
    
    scores['total'] = sum(scores.values())
    weakest = min(scores.items(), key=lambda x: x[1])
    scores['weakest_pillar'] = weakest[0]
    scores['weakest_score'] = weakest[1]
    
    return scores


def compute_insights(data):
    """Compute leverage scores, CTR opportunities, position buckets, freshness flags."""
    pages = data["gsc"]["pages"]
    content_posts = {p["slug"]: p for p in data["content"]["posts"]}
    today = date.today()

    # Position buckets
    buckets = {"top_3": 0, "top_10": 0, "top_20": 0, "top_50": 0, "top_100": 0}
    for p in pages:
        pos = p["position"]
        if pos <= 3: buckets["top_3"] += 1
        if pos <= 10: buckets["top_10"] += 1
        if pos <= 20: buckets["top_20"] += 1
        if pos <= 50: buckets["top_50"] += 1
        if pos <= 100: buckets["top_100"] += 1

    # CTR opportunity & leverage score per page
    # Expected CTR by position (rough industry benchmarks)
    def expected_ctr(pos):
        if pos <= 3: return 0.15
        if pos <= 5: return 0.08
        if pos <= 10: return 0.05
        if pos <= 15: return 0.03
        if pos <= 20: return 0.02
        if pos <= 30: return 0.01
        return 0.005

    enhanced_pages = []
    for p in pages:
        exp_ctr = expected_ctr(p["position"])
        actual_ctr = p["ctr"] / 100
        potential_clicks = int(p["impressions"] * exp_ctr)
        click_gap = potential_clicks - p["clicks"]
        # Leverage score: impression volume × CTR gap × position penalty
        leverage = p["impressions"] * max(click_gap, 0) * (1 / max(p["position"], 1))

        # Freshness flag
        post = content_posts.get(p["slug"])
        freshness = None
        if post:
            try:
                mtime = datetime.strptime(post["mtime"], "%Y-%m-%d").date()
                age_days = (today - mtime).days
                if age_days > 180:
                    freshness = {"status": "stale", "age_days": age_days, "label": f"{age_days}d old"}
                elif age_days > 90:
                    freshness = {"status": "aging", "age_days": age_days, "label": f"{age_days}d"}
                else:
                    freshness = {"status": "fresh", "age_days": age_days, "label": ""}
            except Exception:
                pass

        enhanced_pages.append({
            **p,
            "potential_clicks": potential_clicks,
            "click_gap": click_gap,
            "leverage": round(leverage),
            "freshness": freshness,
            "seo_score": _score_article(p["slug"]),
            "has_infographic": os.path.exists(os.path.join(PROJECT_DIR, "public", f"hero-{p['slug']}-infographic.png")),
        })

    # Priority actions: top pages by leverage
    priority = sorted(
        [p for p in enhanced_pages if p["click_gap"] > 0 and p["impressions"] >= 100],
        key=lambda p: -p["leverage"]
    )[:5]

    return {
        "position_buckets": buckets,
        "enhanced_pages": enhanced_pages,
        "priority_actions": priority,
    }


# ── HTML Generation ─────────────────────────────────────────────────────────

def color_val(val, threshold_up=0, threshold_down=0):
    """Return CSS color class based on value."""
    if val > threshold_up:
        return "var(--green)"
    elif val < threshold_down:
        return "var(--red)"
    return "var(--text-secondary)"

def trend_arrow(val, up_good=True):
    """Return trend arrow emoji."""
    if val > 0:
        return "📈" if up_good else "📉"
    elif val < 0:
        return "📉" if up_good else "📈"
    return "➡️"

def _cron_health_html(cron_status):
    """Render cron job health table."""
    if not cron_status.get("available"):
        return f'<p style="color:var(--text-muted);font-size:13px">Cron status unavailable: {cron_status.get("error", "unknown")}</p>'

    jobs = cron_status.get("jobs", [])
    if not jobs:
        return '<p style="color:var(--text-muted);font-size:13px">No cron jobs found.</p>'

    total = cron_status["total"]
    ok_count = cron_status["ok"]
    err_count = cron_status["error"]

    summary_color = "var(--green)" if err_count == 0 else "var(--amber)" if err_count <= 2 else "var(--red)"
    summary = f'<p style="margin-bottom:14px;font-size:13px"><span style="color:{summary_color};font-weight:700">{ok_count}/{total} OK</span>'
    if err_count > 0:
        summary += f' <span style="color:var(--red)">{err_count} errors</span>'
    if cron_status.get("never_run", 0) > 0:
        summary += f' <span style="color:var(--text-muted)">{cron_status["never_run"]} pending first run</span>'
    summary += '</p>'

    rows = ""
    for j in jobs:
        status_icon = {"ok": "✅", "error": "🔴", None: "⏳"}.get(j["last_status"], "❓")
        status_color = {"ok": "var(--green)", "error": "var(--red)","" : "var(--text-muted)"}.get(j.get("last_status",""), "var(--text-muted)")
        last_run = j.get("last_run", "never") or "never"
        if last_run != "never" and len(last_run) > 16:
            last_run = last_run[:16]
        error_text = ""
        if j.get("last_error"):
            error_text = f' <span style="color:var(--red);font-size:10px" title="{j["last_error"]}">⚠</span>'
        rows += f"""
            <tr>
                <td style="font-size:12px;color:var(--text)">{j['name']}</td>
                <td style="text-align:center;font-size:11px">{j['schedule']}</td>
                <td style="text-align:center;color:{status_color}">{status_icon}</td>
                <td style="font-size:11px;color:var(--text-muted)">{last_run}{error_text}</td>
            </tr>"""

    return f"""{summary}
    <div class="table-wrap">
        <table>
            <thead><tr><th>Job</th><th>Schedule</th><th>Status</th><th>Last Run</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""


def generate_html(data):
    """Render the full dashboard HTML."""
    gsc = data["gsc"]
    ga4 = data["ga4"]
    content = data["content"]
    deltas = data["deltas"]
    anomalies = data["anomalies"]
    generated = data["generated_at"]
    insights = data.get("insights", {})
    enhanced_pages = insights.get("enhanced_pages", gsc["pages"])
    priority_actions = insights.get("priority_actions", [])
    buckets = insights.get("position_buckets", {})
    cron_status = data.get("cron_status", {"available": False})

    # KPI extraction
    kpi = {
        "clicks": gsc["totals"]["clicks"],
        "impressions": gsc["totals"]["impressions"],
        "ctr": gsc["totals"]["ctr"],
        "sessions": ga4["totals"]["current"]["sessions"],
        "posts": content["total"],
        "engagement": ga4["totals"]["current"]["engagement_rate"],
    }

    # Trend data
    trends = gsc["trend_windows"]

    # Page table with CTR opportunity + freshness
    page_rows_html = ""
    for p in enhanced_pages[:20]:
        ctr_color = "var(--red)" if (p["ctr"] < 1 and p["impressions"] >= 500 and p["position"] <= 15) else \
                    "var(--green)" if p["ctr"] >= 2 else "var(--text-secondary)"
        potential = p.get("potential_clicks", 0)
        opportunity = f"{potential}" if potential > p["clicks"] else ""
        opp_color = "var(--amber)" if opportunity else "var(--text-muted)"
        freshness = p.get("freshness")
        fresh_html = ""
        if freshness and freshness["status"] == "stale":
            fresh_html = f' <span style="color:var(--red);font-size:10px" title="Last updated {freshness["age_days"]} days ago">⚠{freshness["age_days"]}d</span>'
        elif freshness and freshness["status"] == "aging":
            fresh_html = f' <span style="color:var(--amber);font-size:10px">{freshness["age_days"]}d</span>'
        page_rows_html += f"""
            <tr>
                <td class="slug-cell" title="{p['url']}">{p['slug'][:45]}{fresh_html}</td>
                <td>{p['impressions']:,}</td>
                <td>{p['position']}</td>
                <td style="color:{ctr_color}">{p['ctr']}%</td>
                <td>{p['clicks']:,}</td>
                <td style="color:{opp_color}">{opportunity}</td>
            </tr>"""

    # Priority actions section
    priority_html = ""
    if priority_actions:
        for i, pa in enumerate(priority_actions):
            priority_html += f"""
                <div class="priority-row">
                    <span class="priority-rank">#{i + 1}</span>
                    <span class="priority-slug">{pa['slug'][:40]}</span>
                    <span class="priority-stat">{pa['impressions']:,} impr — {pa['clicks']} clicks → ~{pa['potential_clicks']} potential</span>
                    <span class="priority-leverage">Leverage: {pa['leverage']:,}</span>
                </div>"""
    else:
        priority_html = '<p style="color:var(--text-muted);font-size:13px">No high-leverage opportunities detected.</p>'

    # SEO Scorecard — 7-pillar rubric scores
    scorecard_rows = ""
    scored = [p for p in enhanced_pages if p.get("seo_score") and p["seo_score"].get("total", 0) > 0]
    scored.sort(key=lambda p: -(p.get("impressions", 0)))
    for p in scored[:15]:
        sc = p["seo_score"]
        total = sc["total"]
        color = "var(--red)" if total < 70 else ("var(--amber)" if total < 85 else "var(--green)")
        scorecard_rows += f"""
            <tr>
                <td class="slug-cell">{p['slug'][:35]}</td>
                <td style="color:{color};font-weight:700">{total}</td>
                <td>{sc['synthesis']}</td>
                <td>{sc['aeo']}</td>
                <td>{sc['regulatory']}</td>
                <td>{sc['formatting']}</td>
                <td>{sc['technical_seo']}</td>
                <td>{sc['internal_links']}</td>
                <td>{sc['freshness']}</td>
                <td style="font-size:10px;color:var(--text-muted)">{sc['weakest_pillar']} ({sc['weakest_score']})</td>
                <td style="text-align:center">{'✅' if p.get('has_infographic') else '❌'}</td>
            </tr>"""

    # Top queries section
    query_html = ""
    top_queries = gsc.get("queries", [])[:10]
    if top_queries:
        for q in top_queries:
            query_html += f"""
                <div class="query-row">
                    <span class="query-text">{q['query'][:55]}</span>
                    <span class="query-stat">{q['impressions']:,} impr</span>
                    <span class="query-stat">{q['clicks']} clicks</span>
                    <span class="query-stat">pos {q['position']}</span>
                </div>"""

    anomaly_html = ""
    if anomalies:
        for a in anomalies[:6]:
            sev_color = {"high": "var(--red)", "medium": "var(--amber)", "low": "var(--blue)"}.get(a["severity"], "var(--text-secondary)")
            anomaly_html += f"""
                <div class="anomaly-card">
                    <span class="anomaly-badge" style="background:{sev_color}">{a['type'].upper()}</span>
                    <span class="anomaly-severity">{a['severity'].upper()}</span>
                    <p class="anomaly-detail">{a['detail']}</p>
                    <p class="anomaly-action">→ {a['action']}</p>
                </div>"""
    else:
        anomaly_html = '<div class="anomaly-card"><p>No anomalies detected. Everything stable.</p></div>'

    # Channel mix bars
    channel_html = ""
    colors_list = ["var(--blue)", "var(--green)", "var(--purple)", "var(--amber)", "var(--red)", "var(--text-secondary)", "var(--pink)"]
    for i, ch in enumerate(ga4["channels"]):
        color = colors_list[i % len(colors_list)]
        channel_html += f"""
            <div class="channel-row">
                <span class="channel-name">{ch['name']}</span>
                <div class="channel-bar-track">
                    <div class="channel-bar" style="width:{ch['share']}%;background:{color}"></div>
                </div>
                <span class="channel-val">{ch['sessions']} ({ch['share']}%)</span>
            </div>"""

    # Cluster coverage
    cluster_html = ""
    for name, count in sorted(content["by_cluster"].items(), key=lambda x: -x[1]):
        cluster_html += f"""
            <div class="cluster-row">
                <span class="cluster-name">{name}</span>
                <span class="cluster-count">{count} posts</span>
            </div>"""

    # Delta summary for KPI cards
    d_clicks = deltas.get("gsc_clicks", 0)
    d_impr = deltas.get("gsc_impressions", 0)
    d_ctr = deltas.get("gsc_ctr", 0)
    d_sessions = deltas.get("ga4_sessions", 0)

    # Conversion data
    conv = ga4.get("conversions", {})
    conv_total = conv.get("total", 0)
    conv_affiliate = conv.get("affiliate_click", 0)
    conv_trial = conv.get("trial_click", 0)
    conv_lead = conv.get("lead_magnet_download", 0)
    conv_playbook = conv.get("playbook_signup", 0)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TradieAutomate — Dashboard</title>
<style>
:root {{
    --bg: #0b0d12;
    --bg-card: #131620;
    --bg-card-hover: #181d28;
    --border: #1e2533;
    --text: #e4e7ed;
    --text-secondary: #8892a6;
    --text-muted: #5a6478;
    --blue: #3b82f6;
    --green: #22c55e;
    --red: #ef4444;
    --amber: #f59e0b;
    --purple: #8b5cf6;
    --pink: #ec4899;
    --accent: #f97316;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    padding: 24px;
}}
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}}
.header h1 {{
    font-size: 22px;
    font-weight: 700;
    color: var(--accent);
}}
.header .generated {{
    font-size: 12px;
    color: var(--text-muted);
}}
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-bottom: 28px;
}}
.kpi-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px;
}}
.kpi-label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.02em;
}}
.kpi-delta {{
    font-size: 12px;
    margin-top: 4px;
}}
.kpi-delta.up {{ color: var(--green); }}
.kpi-delta.down {{ color: var(--red); }}
.kpi-delta.flat {{ color: var(--text-muted); }}

.section {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 22px;
    margin-bottom: 20px;
}}
.section h2 {{
    font-size: 15px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 16px;
    letter-spacing: 0.02em;
}}

/* Trend chart */
/* Trend cards */
.trend-cards {{
    display: flex;
    gap: 14px;
}}
.trend-card {{
    flex: 1;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 16px;
    text-align: center;
}}
.trend-card-date {{
    font-size: 10px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
}}
.trend-card-impr {{
    font-size: 24px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
}}
.trend-card-label {{
    font-size: 10px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
}}
.trend-card-clicks {{
    font-size: 15px;
    font-weight: 600;
    color: var(--green);
}}
.trend-card-ctr {{
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 4px;
}}

/* Table */
.table-wrap {{
    overflow-x: auto;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}
th {{
    text-align: left;
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    color: var(--text-muted);
    font-weight: 500;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
td {{
    padding: 10px 12px;
    border-bottom: 1px solid rgba(30, 37, 51, 0.5);
}}
tr:hover td {{ background: rgba(255,255,255,0.02); }}
.slug-cell {{
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 12px;
    color: var(--text-secondary);
}}

/* Anomalies */
.anomaly-card {{
    background: rgba(239, 68, 68, 0.05);
    border: 1px solid rgba(239, 68, 68, 0.15);
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 10px;
}}
.anomaly-badge {{
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    color: #fff;
    margin-right: 8px;
}}
.anomaly-severity {{
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 600;
}}
.anomaly-detail {{
    margin-top: 8px;
    font-size: 13px;
    color: var(--text);
}}
.anomaly-action {{
    margin-top: 6px;
    font-size: 12px;
    color: var(--amber);
}}

/* Channels */
.channel-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}}
.channel-name {{
    font-size: 12px;
    color: var(--text-secondary);
    width: 130px;
    flex-shrink: 0;
}}
.channel-bar-track {{
    flex: 1;
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
}}
.channel-bar {{
    height: 100%;
    border-radius: 4px;
    transition: width 0.4s;
}}
.channel-val {{
    font-size: 12px;
    color: var(--text-muted);
    width: 100px;
    text-align: right;
    flex-shrink: 0;
}}

/* Clusters */
.cluster-row {{
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid rgba(30, 37, 51, 0.3);
}}
.cluster-name {{
    font-size: 12px;
    color: var(--text-secondary);
}}
.cluster-count {{
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 600;
}}

.grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}}
@media (max-width: 900px) {{
    .grid-2 {{ grid-template-columns: 1fr; }}
}}

.tracking-warning {{
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 12px;
    color: var(--amber);
    margin-top: 12px;
}}

/* Priority actions */
.priority-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(30, 37, 51, 0.3);
}}
.priority-rank {{
    font-size: 14px;
    font-weight: 700;
    color: var(--accent);
    width: 24px;
    flex-shrink: 0;
}}
.priority-slug {{
    font-size: 12px;
    color: var(--text);
    font-family: 'SF Mono', 'Fira Code', monospace;
    width: 180px;
    flex-shrink: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.priority-stat {{
    font-size: 12px;
    color: var(--text-secondary);
    flex: 1;
}}
.priority-leverage {{
    font-size: 11px;
    color: var(--amber);
    font-weight: 600;
    flex-shrink: 0;
}}

/* Query rows */
.query-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0;
    border-bottom: 1px solid rgba(30, 37, 51, 0.2);
}}
.query-text {{
    font-size: 12px;
    color: var(--text-secondary);
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.query-stat {{
    font-size: 11px;
    color: var(--text-muted);
    flex-shrink: 0;
    width: 70px;
    text-align: right;
}}

/* Position buckets */
.pos-buckets {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}}
.pos-bucket {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 12px;
    text-align: center;
    flex: 1;
    min-width: 60px;
}}
.pos-bucket-num {{
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
}}
.pos-bucket-label {{
    font-size: 10px;
    color: var(--text-muted);
    text-transform: uppercase;
}}
</style>
</head>
<body>

<div class="header">
    <h1>⚡ TradieAutomate Dashboard</h1>
    <div class="generated" style="display:flex;align-items:center;gap:16px">
        <span>Generated: {generated}</span>
        <a href="obsidian://open?vault=MyObsidianVault&file=Projects%2FTradieAutomate%2FTeam%2FDashboard" style="color:var(--accent);text-decoration:none;font-weight:600;font-size:12px">👥 Virtual Team →</a>
    </div>
</div>

<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">Clicks (28d)</div>
        <div class="kpi-value">{kpi['clicks']:,}</div>
        <div class="kpi-delta {'up' if d_clicks > 0 else 'down' if d_clicks < 0 else 'flat'}">{trend_arrow(d_clicks)} {d_clicks:+d}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Impressions (28d)</div>
        <div class="kpi-value">{kpi['impressions']:,}</div>
        <div class="kpi-delta {'up' if d_impr > 0 else 'down' if d_impr < 0 else 'flat'}">{trend_arrow(d_impr)} {d_impr:+,}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Avg CTR</div>
        <div class="kpi-value" style="color:{'var(--green)' if kpi['ctr'] >= 1.5 else 'var(--red)'}">{kpi['ctr']}%</div>
        <div class="kpi-delta {'up' if d_ctr > 0 else 'down' if d_ctr < 0 else 'flat'}">{trend_arrow(d_ctr)} {d_ctr:+.2f}%</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Sessions (28d)</div>
        <div class="kpi-value">{kpi['sessions']:,}</div>
        <div class="kpi-delta {'up' if d_sessions > 0 else 'down' if d_sessions < 0 else 'flat'}">{trend_arrow(d_sessions)} {d_sessions:+d}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Indexed Posts</div>
        <div class="kpi-value">{kpi['posts']}</div>
        <div class="kpi-delta flat">Last: {content['last_updated'] or '—'}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Engagement Rate</div>
        <div class="kpi-value">{round(kpi['engagement'] * 100)}%</div>
        <div class="kpi-delta flat">GA4: {'✅ tracking active' if conv_total > 0 else '✅ active — 0 conversions yet'}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Conversions (28d)</div>
        <div class="kpi-value" style="color:{'var(--green)' if conv_total > 0 else 'var(--text-muted)'}">{conv_total}</div>
        <div class="kpi-delta flat">Trial: {conv_trial} | Lead: {conv_lead} | Playbook: {conv_playbook}</div>
    </div>
</div>

<!-- Trend Chart -->
<div class="section">
    <h2>📈 3-Month Impression & Click Trend</h2>
    <div class="trend-cards">
        {''.join(f'''
        <div class="trend-card">
            <div class="trend-card-date">{w['start'][5:]} to {w['end'][5:]}</div>
            <div class="trend-card-impr">{w['impressions']:,}</div>
            <div class="trend-card-label">impressions</div>
            <div class="trend-card-clicks">{w['clicks']} clicks</div>
            <div class="trend-card-ctr">{round(w['clicks'] / max(w['impressions'], 1) * 100, 2)}% CTR</div>
        </div>''' for w in reversed(trends))}
    </div>
</div>

<!-- Anomalies -->
<div class="section">
    <h2>⚠️ Anomalies & Action Items</h2>
    {anomaly_html}
</div>

<!-- Priority Actions -->
<div class="section">
    <h2>🎯 Priority Actions (ranked by leverage)</h2>
    <p style="font-size:11px;color:var(--text-muted);margin-bottom:12px">Pages with the highest impression × CTR-gap opportunity. Fix these first.</p>
    {priority_html}
</div>

<!-- Position Buckets -->
<div class="section">
    <h2>📍 Position Distribution <span style="font-size:11px;color:var(--text-muted);font-weight:400">(Page 1 = positions 1–10)</span></h2>
    <div class="pos-buckets">
        <div class="pos-bucket"><div class="pos-bucket-num">{buckets.get('top_3', 0)}</div><div class="pos-bucket-label">Top 3</div></div>
        <div class="pos-bucket" style="border-color:var(--green)"><div class="pos-bucket-num">{buckets.get('top_10', 0)}</div><div class="pos-bucket-label">Page 1</div></div>
        <div class="pos-bucket"><div class="pos-bucket-num">{buckets.get('top_20', 0)}</div><div class="pos-bucket-label">Page 2</div></div>
        <div class="pos-bucket"><div class="pos-bucket-num">{buckets.get('top_50', 0)}</div><div class="pos-bucket-label">Page 5</div></div>
        <div class="pos-bucket"><div class="pos-bucket-num">{buckets.get('top_100', 0)}</div><div class="pos-bucket-label">Page 10</div></div>
    </div>
</div>

<!-- Cron Health -->
<div class="section">
    <h2>🤖 Automation Health</h2>
    {_cron_health_html(cron_status)}
</div>

<!-- Page Performance -->
<div class="section">
    <h2>📊 Top Pages by Impressions (28d)</h2>
    <div class="table-wrap">
        <table>
            <thead><tr><th>Page</th><th>Impressions</th><th>Position</th><th>CTR</th><th>Clicks</th><th>CTR Opp</th></tr></thead>
            <tbody>{page_rows_html}</tbody>
        </table>
    </div>
</div>

<!-- SEO Scorecard -->
<div class="section">
    <h2>📝 Article Quality Scorecard (7-Pillar Rubric)</h2>
    <p style="font-size:12px;color:var(--text-muted);margin-bottom:8px">Top 15 by impression volume. 🟢 85+ 🟠 70-84 🔴 <70 | SYN=Synthesis AEO=Answer Engine REG=Regulatory FMT=Formatting SEO=Technical LINK=Internal FRESH=Freshness IMG=Infographic</p>
    <div class="table-wrap">
        <table>
            <thead><tr><th>Article</th><th>Score</th><th>SYN</th><th>AEO</th><th>REG</th><th>FMT</th><th>SEO</th><th>LINK</th><th>FRESH</th><th>Weakest</th><th>IMG</th></tr></thead>
            <tbody>{scorecard_rows if scorecard_rows else '<tr><td colspan="10" style="color:var(--text-muted)">No scores available — run dashboard generator to populate.</td></tr>'}</tbody>
        </table>
    </div>
</div>

<div class="grid-2" style="grid-template-columns:1fr 1fr 1fr\">
    <!-- Traffic Mix -->
    <div class="section">
        <h2>🌐 Traffic Sources</h2>
        {channel_html}
        {'<div class="tracking-warning">📊 GA4 event tracking is active (trial_click_1, lead_magnet_download, playbook_signup). Zero conversions recorded — Data API has 24-48h latency and these are high-intent actions.</div>' if conv_total == 0 else ''}
    </div>

    <!-- Top Queries -->
    <div class="section">
        <h2>🔍 Top Search Queries</h2>
        {query_html if query_html else '<p style="color:var(--text-muted);font-size:13px">No query data available.</p>'}
    </div>

    <!-- Content Clusters -->
    <div class="section">
        <h2>📝 Content by Cluster</h2>
        <p style="font-size:24px;font-weight:700;margin-bottom:12px">{content['total']} posts</p>
        {cluster_html}
    </div>
</div>

</body>
</html>"""
    return html


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print("📊 TradieAutomate Dashboard Generator")
    print("=" * 50)

    # 1. Pull GSC
    print("\n🔍 Pulling GSC data...")
    try:
        gsc_data = pull_gsc_data()
        print(f"   {gsc_data['totals']['clicks']} clicks, {gsc_data['totals']['impressions']:,} impressions, "
              f"{gsc_data['totals']['ctr']}% CTR, {len(gsc_data['pages'])} pages")
    except Exception as e:
        print(f"   ❌ GSC pull failed: {e}")
        gsc_data = {"pages": [], "queries": [], "trend_windows": [], "totals": {"clicks": 0, "impressions": 0, "ctr": 0, "avg_position": 0, "pages_with_data": 0}}

    # 2. Pull GA4
    print("📈 Pulling GA4 data...")
    try:
        ga4_data = pull_ga4_data()
        print(f"   {ga4_data['total_sessions']} sessions, {len(ga4_data['channels'])} channels, "
              f"tracking_gap={ga4_data['tracking_gap']}")
    except Exception as e:
        print(f"   ❌ GA4 pull failed: {e}")
        ga4_data = {"totals": {"current": {}, "prior": {}}, "tracking_gap": True, "top_pages": [], "channels": [], "total_sessions": 0}

    # 2b. Pull GA4 conversion events
    print("🎯 Pulling GA4 conversion events...")
    try:
        conversions = pull_ga4_conversions()
        ga4_data["conversions"] = conversions
        print(f"   {conversions['total']} total conversion events: "
              f"affiliate={conversions['affiliate_click']}, trial={conversions['trial_click']}, "
              f"lead_magnet={conversions['lead_magnet_download']}, playbook={conversions['playbook_signup']}")
    except Exception as e:
        print(f"   ⚠️ GA4 conversions pull failed: {e}")
        ga4_data["conversions"] = {"affiliate_click": 0, "trial_click": 0, "lead_magnet_download": 0, "playbook_signup": 0, "total": 0}

    # 3. Analyze content
    print("📝 Analyzing content...")
    content = analyze_content()
    print(f"   {content['total']} posts, {len(content['by_cluster'])} clusters, last updated: {content['last_updated']}")

    # 4. Assemble today's data
    today = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S AEST"),
        "gsc": gsc_data,
        "ga4": ga4_data,
        "content": content,
    }

    # 5. Load yesterday's data (if exists)
    yesterday = None
    if os.path.exists(DASHBOARD_JSON):
        try:
            with open(DASHBOARD_JSON) as f:
                yesterday = json.load(f)
            # Only use yesterday if it's from a different calendar day
            yesterday_date = yesterday.get("generated_at", "")[:10]
            today_date = today["generated_at"][:10]
            if yesterday_date == today_date:
                yesterday = None  # Same day, don't compare against ourselves
        except Exception:
            yesterday = None

    # 6. Compute deltas & anomalies
    deltas, anomalies = compute_deltas(today, yesterday)
    today["deltas"] = deltas
    today["anomalies"] = anomalies
    print(f"\n📊 Deltas: clicks {deltas['gsc_clicks']:+d}, impressions {deltas['gsc_impressions']:+,}, "
          f"CTR {deltas['gsc_ctr']:+.2f}%, sessions {deltas['ga4_sessions']:+d}")
    print(f"⚠️  Anomalies: {len(anomalies)} found")

    # 7. Compute insights (leverage scores, CTR opportunities, position buckets, freshness)
    insights = compute_insights(today)
    today["insights"] = insights

    # 7b. Pull cron job status
    cron_status = pull_cron_status()
    today["cron_status"] = cron_status
    if cron_status.get("available"):
        print(f"🤖 Cron health: {cron_status['ok']}/{cron_status['total']} OK, {cron_status['error']} errors, {cron_status['never_run']} never run")
    else:
        print(f"🤖 Cron status unavailable: {cron_status.get('error', 'unknown')}")

    # 8. Write dashboard.json
    with open(DASHBOARD_JSON, "w") as f:
        json.dump(today, f, indent=2, default=str)
    print(f"\n✅ dashboard.json written ({os.path.getsize(DASHBOARD_JSON):,} bytes)")

    # 9. Generate HTML
    html = generate_html(today)
    with open(DASHBOARD_HTML, "w") as f:
        f.write(html)
    print(f"✅ dashboard.html written ({os.path.getsize(DASHBOARD_HTML):,} bytes)")

    print(f"\n🎯 Done. Open with: open {DASHBOARD_HTML}")


if __name__ == "__main__":
    main()
