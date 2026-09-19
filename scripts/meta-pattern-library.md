# Meta Pattern Library — from real SERP competitor analysis
# 151 competitor entries across 20 TradieAutomate target queries.
# Each pattern below has a real winning example and a template.
# The cron references this file when generating meta rewrites.

## Pattern A: The "Honest Review" (for comparison/review queries)
Real examples:
- "ServiceM8 Review 2026: Honest Pros, Cons & Pricing"
- "CCEW Review 2026: Pros, Cons, Features & Pricing" 
Template: "[Product] [Year]: Honest Pros, Cons & [Differentiator]"
When to use: Review and comparison queries where the searcher is deciding

## Pattern B: The "Year + Feature" (for software/search queries)
Real examples:
- "Best Electrical Contractor Software 2026 | Estimating, Invoice, Scheduling"
- "ServiceM8 Update 2026: New Features & Launch Event"
Template: "Best [Category] [Year] | [Feature1], [Feature2], [Feature3]"
OR: "[Topic] [Year]: [What Changed], [What's New], [Key Detail]"
When to use: Software comparisons, tool evaluations, category searches

## Pattern C: The "Action Guide" (for compliance/how-to queries)
Real examples:
- "Certificate of Compliance for Electrical Work (CCEW) form" (nsw.gov.au)
- "Electrical Certificate of Compliance: Costs, Rules & Missing Certificates"
- "Electrical Compliance Certificate NSW: When You Need One"
Template: "[Topic]: [Action Frame] — [Costs/Rules/Key Detail]"
When to use: Compliance, licensing, regulatory queries

## Pattern D: The "Question Hook" (for informational queries)
Real examples:
- "What is a Certificate of Compliance for Electrical Work?"
- "Is ServiceM8 Worth It? [Year] Honest Review"
Template: "[Question about [Topic]]? [Year] [Honest/Complete] [Frame]"
When to use: Broad informational queries, definitional searches

## Pattern E: The "Year + Cost/Rules" (for compliance queries)
Real examples:
- "Electrical Certificate of Compliance VIC: Cost & 2026 Rules"
- "Certificate of Electrical Safety: Fees, Deadlines & Compliance Guide [Year]"
Template: "[Topic] [Year]: Fees, [Deadline/Rule], & [Guide Type]"
When to use: Compliance pages with a cost or deadline angle

## Pattern F: The "Comparison vs" (for head-to-head queries)
Real examples:
- "ServiceM8 vs Jobber vs ???"
- "Tradify vs ServiceM8: Which Is Better?"
Template: "[ProductA] vs [ProductB] [Year]: Which Is Better for [Use Case]?"
When to use: Direct comparison queries

## Pattern G: The "Authority/Definition" (reserved for .gov domains)
Real examples:
- "Certificate of Compliance for Electrical Work (CCEW) form" (nsw.gov.au)
- "Certificates of Electrical Safety - Energy Safe Victoria" (gov site)
Do NOT use this pattern on tradieautomate.com — it only works for government domains.

## Selection rules (applied by cron, in order):
1. If the query is a comparison query (contains "vs", "versus", "or"): use Pattern A or F
2. If the page is a compliance page (slug contains: licence, ccew, ces, rcd, compliance, safety): use Pattern C or E
3. If the query is a software/tool name: use Pattern B or A
4. If the query is informational (what is, how to): use Pattern D
5. Always prefer putting the year in the title
6. Never use "What It Is & Who Issues It" — this pattern produces 0.5-1% CTR
7. When in doubt, check the competitor database (`scripts/competitor_metas.json`) for the exact query and mirror the top result's INTENT, not its wording

## Meta description rules (universal):
1. Lead with the KEY ACTION — not "[Topic] is a..."
2. Every description must have a dollar figure, deadline, or specific number
3. 120-160 chars. Below 120 = thin. Above 160 = truncated.
4. No fear framing. "Penalties" is factual. "Avoid $22K fines" on a process query kills CTR.
5. End with a "guide" or "step-by-step" signal if the page is structured that way.
6. For comparison reviews: mention the specific differentiator ($29/mo, for crew size X)
7. For compliance: mention the fee/deadline (from $X, within Y days)
8. For lookup: mention the specific data point (X% rate, $X per hour)