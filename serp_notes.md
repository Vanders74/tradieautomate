# SERP rank monitor - notes log

Context per keyword check. `keyword_ranks.csv` holds the numbers; this file explains them.
Rotation state: `serp_state.json` (next_index, cycle). Canonical domain: **tradieautomate.com** (Netlify).

## Cycle 1

### 1. how to price solar installations australia - 2026-10-23 - rank >20
- Target page: /blog/how-to-price-solar-installations-australia-2026/ (live, 200, canonical set, indexed).
- Not in top 20 on Bing-backed or Google results. Top 20 is entirely consumer-intent cost content
  (SolarQuotes, Solar Choice, Canstar, hipages, energy.gov.au, EcoFlow, Why Solar, Greenlight).
- Diagnosis: head term is read by Google as a homeowner query. It is not an installer query.
- Proof the page is healthy: for installer-intent phrasing
  "how to price solar jobs as an installer profit margin australia" it ranks **#4**
  (hidden-costs article #3 above it). Both pages are indexed and competing where intent matches.
- Action worth taking: stop chasing the head term; build/cannibalise around installer-intent
  variants ("solar installer profit margin", "how to quote a solar job", "solar quote template")
  where the page already sits page 1. Competitors now in that space: whysolar.com.au (industry
  benchmark pages), flowspec.com.au, solproof.com.au, quotemateapp.au, uprisedigital.com.au.
- Data caveat: Google render was degraded (report said "About 133 results", ~11 organic snippets
  returned), so treat ">20" as "not seen in top 20", not an exact position.

### 20. electrical contractor award rates australia - 2026-10-23 - rank 5
- Page 1 mid-pack against Fair Work, AwardScale, Valont, VeriTradie, ECA WA. Rate-table snippet holding.

## Domain note (2026-10-23)
- tradieautomate.com.au resolves to 103.42.108.46 and serves a parked "Your Domains" page over
  HTTP; HTTPS fails the TLS handshake entirely. It is not the live site and is not referenced
  anywhere in the repo. Only a problem if anything external links or cites the .com.au spelling,
  or if you intended to own it. Worth checking the registrar.
