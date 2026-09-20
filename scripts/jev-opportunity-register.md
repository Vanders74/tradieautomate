# Jev AI Opportunity Register — TradieAutomate
Assessment Date: 2026-09-20
Status: Pre-quota — recorded for when Jev becomes available post free-tier

## What Jev is for TradieAutomate

Jev is not a content generator. It is a **decision model** — classifies, scores, and routes
faster and cheaper than an LLM for any task that doesn't need text output. Every application
below replaces something currently done by: (a) me manually, (b) an expensive DeepSeek cron
call, or (c) not done at all because it costs too much to run regularly.

Assessment: ROI = time saved × accuracy gain × frequency. Feasibility = how easy to wire in.

---

## DONE — Already in dashboard, just needs more quota to finish

### 1. SEO Intent Classification ⭐⭐⭐⭐⭐
**What:** Classifies each page's intent (lookup/compliance/comparison/strategy) from title+meta.
**Pain solved:** The Zero-CTR cron currently burns DeepSeek calls analyzing each page's intent
one at a time. Jev does it in batch for ~$0.01 per full site audit.
**Status:** 32/123 pages classified before free-tier quota ran out. Remaining 91 need ~3 minutes.
**Future:** Once classified, the data lives in dashboard.json. The striking-distance engine checks
`enhanced_pages[n].jev.intent` instead of calling DeepSeek. Zero ongoing cost.

---

## PHASE 1 — Wire in when Jev is available (1-2 hours each)

### 2. Query-to-Page Intent Match Check ⭐⭐⭐⭐⭐
**What:** For each GSC query + the page it ranks, ask Jev: "Does this query's intent match this page's
intent?" Returns yes/no + confidence.
**Value:** The cron currently infers this from the page meta. With Jev, we'd know exactly which
queries are landing on the wrong page — the true zero-click cause.
**Implementation:** After dashboard generator pulls GSC data, batch-classify all query-page pairs.
Store as `query_intent_matches[]` in insights.
**Cost:** ~$0.005 per batch (500 queries × ~30 tokens × $0.042/MTok).

### 3. Content Gap Discovery ⭐⭐⭐⭐
**What:** Take GSC queries with impressions but NO matching page slug. Ask Jev: "Which content
category does this fit?" (from our 6 categories). Group by category. Surface highest-volume
unanswered queries as a priority.
**Pain solved:** Currently we only fix pages that *already exist*. Jev finds whole content
clusters we haven't written. This is how we discovered the AI data-centre pillar.
**Implementation:** After GSC pull, filter queries by "no blog page slug matches this query."
Feed top 50 to Jev. Store as `content_gaps[]` in dashboard.
**Cost:** ~$0.002 per batch.

### 4. Content Decay Flagging ⭐⭐⭐
**What:** Feed each page's title + opening paragraph. Ask Jev: "Does this reference specific 2026
data (rates, standards, deadlines) or is it evergreen?" Returns evergreen/specific + confidence.
**Pain solved:** Not all stale content decays equally. A "What is a CCEW" guide is evergreen.
A page citing "2024 rates" is decaying. Jev separates them so the cron prioritises actual
decay over surface staleness.
**Implementation:** Slot into the existing freshness scoring in `compute_insights`.

### 5. Priority Scoring Reweight ⭐⭐⭐
**What:** Current leverage formula = imp × click_gap × 1/position. Jev adds: intent mismatch flag,
meta quality score, missing stakes signal. Combined into a single calibrated urgency score.
**Pain solved:** The cron picks top-5 by leverage, but they're sometimes the wrong 5 — pages
with decent metas but high impression volume. Jev-reweighted priority surfaces true
intent-mismatch pages first.
**Implementation:** Change the sort key in `compute_insights()` priority section.

### 6. Repurposing Decision Engine ⭐⭐⭐
**What:** Take top 10 pages by impressions. Ask Jev: "Best format for this page — video script,
newsletter, PDF lead magnet, or social thread?" Returns best format + confidence.
**Pain solved:** We do zero repurposing today because we don't know where to start. Jev gives us
the first cut — which pages to repurpose, and into what format.
**Implementation:** Standalone script, runs after dashboard build.

---

## PHASE 2 — Larger projects (4-8 hours each)

### 7. Internal Link Opportunity Detection ⭐⭐
**What:** For each page section, ask Jev: "Which of these 5 related pages could this paragraph link to?"
**Verdict:** Better done with embeddings (cosine similarity) than Jev. Jev's 32K context means
we can only check ~5 candidates per call. 146 pages × each other = ~20,000 calls — too many.
**Decision:** Backburner. Revisit when we have an embedding pipeline.

---

## YOUR SUGGESTIONS — Assessed

| Idea | Verdict | Why |
|---|---|---|
| Publishing Traffic Light | ⭐⭐ | We publish 0-1/week. SEO rubric already gates quality. Worth at 3+/week. |
| Jargon & Tone Check | ⭐ | We already write in tradie voice. Content agent knows the guidelines. |
| Lead & Comment Scoring | ⭐ | 14 conversions/month. Manual triage is sufficient. |
| Trade Niche Sorting | ⭐ | ~0 subscriber signups. Premature. |
| Smart Content Routing | ⭐ | No reader profiles. Premature. |
| Spam & Link-Farm Filter | ⭐ | ~0 comments. Wait for volume. |
| High-Intent Alerts | ⭐ | No real-time sales pipeline. Premature. |
| Social Hook Selector | ⭐⭐ | 3 posts/week. Manual works fine at this scale. |
| Outreach Relevance Check | ⭐ | No outbound pipeline. Prature. |
| Channel Distribution Router | ⭐⭐ | 2 channels (FB, IG). 30-second manual choice per post. |
| UGC / Testimonial Selector | ⭐ | No UGC pipeline. |
| Terminology Localiser (AU vs US) | ⭐⭐ | Handled manually ~once/month. Not worth automation. |
| LLM Cost Router | ⭐⭐⭐ | Already happening conceptually. Jev IS the cheap layer. |
| Prompt Noise Cleaner | ⭐⭐ | Niche. Can strip fluff before sending to DeepSeek. Rarely needed. |
| Competitor Content Alerts | ⭐⭐ | Needs fresh SERP data + high maintenance. Not worth it now. |

---

## PRIORITY ORDER (when quota becomes available)

1. **Classify remaining 91 pages** (already wired, 3 minutes runtime)
2. **Query-to-Page Intent Match** (fixes the Zero-CTR root cause)
3. **Content Gap Discovery** (finds new article opportunities)
4. **Repurposing Decision Engine** (opens a new distribution channel)
5. **Content Decay Flagging** (better freshness priority)
6. **Priority Scoring Reweight** (better cron decisions)

Items 7+ in the backburner file until volume or pipeline justifies them.