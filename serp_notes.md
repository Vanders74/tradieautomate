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

### 2. ev charger installation cost australia - 2026-10-23 - rank >20
- Target page: /blog/ev-charger-installation-cost-australia-2026/ (live 200, canonical correct, title
  "EV Charger Installation Cost Australia 2026: What Electricians Charge and Why", indexed).
- Not in the 20 results returned. Top 20 is pure homeowner cost content: RAA, RACV, RAC WA, Revcharge,
  PumpSwap (owns 3 slots incl. a state cost index), Gridly (2 slots), SolarQuotes, Solar Choice price
  index, zecar, evse.com.au, EV Roadside, quick-quote, goingrate, whatsthedamage, faircost.
- Same pattern as keyword 1: the query is homeowner intent, our page is installer intent. Where the
  intent matches, we rank well — "how much should an electrician charge to install an EV charger
  australia profit margin" returns /blog/ev-charger-installation-electricians-australia-2026/ at #1,
  the network-business guide at #4 and the cost article at #10.
- **New finding - the tool page is invisible.** "ev charger quote calculator electricians australia"
  returns heyjodie.com/en-au/tools/ev-charger-installation-cost-calculator/ at #1 (calculator for
  electricians, installer-facing copy). Our /tools/ev-charger-quote-calculator/ does not appear at all,
  and its H1 is still homeowner-facing: "How Much Does EV Charger Installation Cost in Australia?".
  The URL and body are installer content, the title/H1 are consumer content - it is optimised for a
  query we cannot win and invisible for the one we can.
- Action worth taking: retitle the tool page to installer intent ("EV Charger Quote Calculator for
  Electricians - Price the Job in 30 Seconds"), keep the existing ranges, add a "quote this job" CTA
  into the ServiceM8 trial. That is a title/H1 change, not a rebuild.
- Cannibalisation risk: 7 EV blog pages + 1 EV tool all bidding on overlapping cost/quote terms.
  Only one should own "installation cost" (the cost article); the tool should own "quote calculator"
  and link to the cost article rather than restate its table.
- Competitor note: FlowSpec and thequoteyard.com.au now both publish installer pricing/margin guides,
  and thequoteyard's covers material markup + fixed-price quoting - same territory as our pricing pages.

### 3. best job management software electricians australia - 2026-10-23 - rank 2
- Target page: /blog/best-job-management-software-electricians-australia/ (200, canonical correct,
  title "Best Job Management Software for Electricians Australia 2026", H1 matches, FAQPage + Article
  schema, published 2026-04-14, modified 2026-10-20). First page-1 hit of the cycle.
- Top 20: webblend.au #1, us #2, heyjodie #3, taskrs #4, sprintsuite #5, tradieappfinder #6, fergus.com #7,
  servicescale #8, itrade #9, stackpick #10, capterra (2 slots), tradify, quotemate (2), kynection,
  simpro blog, connecteam, onebookplus.
- **The #1 result is a threat, not a fluke.** webblend.au published their electrician job-management
  page **2026-09-13** (5 weeks old) and took #1 over a page that has been live since April. They are an
  Australian web/automation shop and a **ServiceM8 partner** - direct competitor for the same reader and
  the same affiliate ground. Their page beats ours on framing, not depth:
  - Title: "An Honest Australian Rundown" vs our "Top 5 Platforms Ranked".
  - A **Quick answer** block above the fold (five options, decided by staff count and work type); our
    page has no answer summary - first H2 is "What Electrical Job Management Software Has to Do", and
    the ranking H2 is "Top 5 Platforms Ranked" followed by "ServiceM8 Deep Dive" and "Our Recommendation",
    i.e. it reads as an affiliate listicle to both Google and a reader.
  - Dated price verification inline ("$48/$52/$62 ex GST as checked on their pricing page in August 2026").
    Ours states prices without a checked-on date.
  - Per-page **AI-summary block plus ChatGPT / Claude / Perplexity deep-link CTAs**, i.e. built to be the
    cited source in AI answers, not just a blue link. We have zero of this across the site.
- They also run a wider cluster on our exact audience (simpro price increase 2026, ServiceM8 Office Agent,
  missed call text back, Airtasker for tradies, GoHighLevel for tradies, websites for electricians) plus a
  /wiki/guides/ hub that aggregates the guides for citation. This is a topical-authority build, not
  scattered blog posts.
- Action worth taking (rank-preserving, not a rebuild):
  1. Add a 60-word "Quick answer" block directly under the H1 with the size-based verdict.
  2. Rename "Top 5 Platforms Ranked" to a neutral verdict heading and add the "checked on" date to every price.
  3. Add the AI-summary + LLM-link block pattern from webblend to this page first, then template it.
- Cannibalisation note: our own brand search returns 5 tradieautomate URLs in the top 10 (this page,
  /blog/servicem8-for-electricians/, sparkys-playbook ch8, servicem8-vs-jobber, servicem8-review-2026).
  Split link equity rather than a single strong cluster page - the wiki-hub pattern is the fix, if we build one.

### 20. electrical contractor award rates australia - 2026-10-23 - rank 5
- Page 1 mid-pack against Fair Work, AwardScale, Valont, VeriTradie, ECA WA. Rate-table snippet holding.

## Domain note (2026-10-23)
- tradieautomate.com.au resolves to 103.42.108.46 and serves a parked "Your Domains" page over
  HTTP; HTTPS fails the TLS handshake entirely. It is not the live site and is not referenced
  anywhere in the repo. Only a problem if anything external links or cites the .com.au spelling,
  or if you intended to own it. Worth checking the registrar.
