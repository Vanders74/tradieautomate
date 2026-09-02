---
title: 'WA Solar Connection: Western Power Export Limits, 30kVA Rule & CSIP-AUS Requirements'
description: "Connect solar in WA via Western Power — 5kW max export (1.5kW static fallback), 30kVA inverter limit from 1 May 2026, CSIP-AUS and emergency solar management."
pubDate: 'Aug 31 2026'
updatedDate: 'Aug 31 2026'
category: "Grid Connection"
heroImage: '/hero-wa-western-power-solar-connection-guide-2026.jpg'
faq:
  - question: "Who is the electricity distributor in Western Australia?"
    answer: "Western Power is the sole electricity distributor for the South West Interconnected System (SWIS) — the main grid covering Perth and the south-west. The SWIS is an isolated grid, not part of the National Electricity Market. Synergy is the retailer for most WA households (a separate role from the distributor). Regional and remote WA outside the SWIS is served by Horizon Power."
  - question: "What are the solar export limits in Western Australia?"
    answer: "Western Power applies a maximum export limit of 5kW for standard single-phase and three-phase connections, but only where the customer has an offtake agreement with their energy retailer (such as the Distributed Energy Buyback Scheme). Without an offtake agreement, export is capped at a static 1.5kW regardless of inverter size. Export is measured nett at the connection point — it is a site total, not a per-phase limit."
  - question: "What changed on 1 May 2026 for WA solar and battery systems?"
    answer: "From 1 May 2026, the WEM Procedure allows inverter energy systems up to a 30kVA aggregate capacity under a standard connection (single and three-phase). All new and upgraded systems must be capable of remote disconnect and reconnect by the retailer — commonly called emergency solar management — or be export-limited to 1.5kW. Inverters must comply with AS/NZS 4777.2:2020 with the grid code set to Australia Region B, and Synergy customers are commissioned using CSIP-AUS."
  - question: "What protocol does WA use — CSIP-AUS or SEP2?"
    answer: "WA uses CSIP-AUS (Common Smart Inverter Profile — Australia), the same open-source communications protocol as South Australia. Synergy customers have their systems commissioned using CSIP-AUS. This differs from Queensland, which uses the IEEE 2030.5 SEP2 protocol for its dynamic connections."
  - question: "Are flexible or dynamic exports available in Western Australia?"
    answer: "Not as a standard mandatory offer yet. WA is building toward flexible exports through Western Power's Dynamic Operating Envelopes, virtual power plants, and Project Jupiter, which will let export limits vary with network conditions. Until then, most customers export on a fixed 5kW limit (with an offtake agreement) or a 1.5kW static fallback."
  - question: "Do I need emergency solar management (remote disconnect) on a WA system?"
    answer: "Yes, if the customer has an offtake agreement with their retailer (such as DEBS). Emergency solar management has applied to DEBS customers with inverters up to 5kVA since 2022, and under the updated requirements it also applies to inverters over 5kVA with an offtake agreement. Customers without an offtake agreement get a static 1.5kW export limit instead."
  - question: "What inverter size can I install in Western Australia?"
    answer: "From 1 May 2026, you can install up to 30kVA aggregate inverter capacity under a standard connection. Single-phase inverters are capped at 10kVA, and three-phase inverters at 15kVA on large networks (a 30kVA inverter must be generation-limited to 15kW). On a three-phase service, a 10kVA single-phase inverter must be generation-limited to 5kW for phase balancing."
  - question: "Do I need a certificate of compliance for a WA solar installation?"
    answer: "Yes. Electrical work in WA is regulated under the Electricity (Licensing) Regulations 1991 (WA), administered by Building and Energy. The licensed electrical contractor must provide the required certificate of compliance for the installation. The Western Power connection approval is separate — both are required."
---

Connecting solar in Western Australia means working with **Western Power** — the distributor for the South West Interconnected System (SWIS), the largest *isolated* grid in the world — and getting two things right: the **export limit** and the **1 May 2026 rule change** that reshaped inverter sizing. WA's export rules are genuinely different from the east-coast states, so quoting off an SA or NSW assumption will cost you.

**Western Power is the sole electricity distributor for the SWIS, the main grid covering Perth and the south-west — and it is not part of the National Electricity Market.** Export is capped at **5kW maximum** for standard connections (with a retailer offtake agreement) and falls to a static **1.5kW** without one. The other headline is the **30kVA aggregate inverter limit** that took effect 1 May 2026, which opened the door to bigger systems while requiring remote disconnect capability (emergency solar management) as the trade-off.

This guide covers the SWIS connection process, the export-limit rules, the 1 May 2026 change, battery and EV requirements, approval timeframes, and the mistakes that get applications knocked back.

---

## Who You're Dealing With: Western Power, Synergy & the SWIS

WA's grid structure is the most distinct in the country, and it matters for how you approach every job.

| Layer | Company | What they do |
|---|---|---|
| Transmission + **Distribution** | **Western Power** | Owns the SWIS network — **approves connections and sets export limits** |
| Retailer | **Synergy** (most households) | Billing, feed-in tariff (DEBS), and emergency solar management |
| Market operator | AEMO | Operates the SWIS wholesale market (an isolated grid, not the NEM) |
| Customer | Your client | The site being connected |

**The SWIS is an isolated grid.** Unlike the east-coast states that plug into the National Electricity Market, the SWIS operates standalone — which is exactly why WA's export and emergency-management rules are stricter. AEMO has to hold the system stable with no neighbouring grid to lean on, and that flows straight down to how much solar you're allowed to export.

**Synergy is the retailer for most homes** (a different role from the distributor). Regional and remote WA outside the SWIS is served by **Horizon Power** — not Western Power — so confirm the site's network before quoting.

---

## Export Limits: The Section That Wins the Job

This is where WA diverges hardest from every other state, and where east-coast assumptions will get you into trouble.

| Export arrangement | Limit | How it works |
|---|---|---|
| **With retailer offtake agreement** (e.g. DEBS) | **5kW maximum** | Requires remote disconnect capability (emergency solar management) |
| **No offtake agreement** | **1.5kW static** | Fixed, all year round, regardless of inverter size |

**The critical WA distinction: export is measured nett at the connection point — it's a site total, not a per-phase limit.** In NSW or QLD, a three-phase home can often export 5kW *per phase* (15kW total). In WA, the 5kW maximum is the *whole site's* export, whether single-phase or three-phase. That's a real quoting difference — a customer moving from a 5kW/phase east-coast assumption to WA gets a 5kW *total* ceiling.

**The 1.5kW fallback is the trap to avoid.** If the customer has no offtake agreement with their retailer, or can't maintain a stable internet connection for remote management, the system is set to a static 1.5kW export — regardless of whether you installed a 6.6kW or 13kW system. Quote the export realistically from the start, not just the panel count.

---

## The 1 May 2026 Rule Change (30kVA + Remote Disconnect)

The biggest shift in WA solar in years took effect **1 May 2026**, under the WEM Procedure for Standard Small User Facilities (connection voltage under 1,000V, aggregate DER capacity of 30kVA or less):

- **30kVA aggregate inverter capacity** — you can now install up to 30kVA of combined solar and battery inverter capacity on a standard connection, up from the previous single-phase 5kVA / three-phase 15kVA limits.
- **Remote disconnect/reconnect required** — every new or upgraded system must be capable of emergency solar management (set up by the installer at installation), unless the customer opts for a fixed 1.5kW export limit instead.
- **AS/NZS 4777.2:2020 with "Australia Region B"** — WA references the 2020 standard with the Australia Region B grid code, which differs from the AS/NZS 4777:2024 editions used in the NEM states. Set the grid code correctly at commissioning.
- **CSIP-AUS commissioning** — Synergy customers are commissioned using the CSIP-AUS protocol (see our [CSIP-AUS and the 1.5kW export limit explainer](/blog/csip-aus-export-limit-1-5kw-solar)).

**What this means in practice:** you can now sell a much larger solar-plus-battery system on a standard connection than you could before May 2026 — but only if it's remotely manageable. The fixed 1.5kW option remains for sites with poor connectivity or customers who don't want to participate in export products.

---

## The SWIS Connection Process

The process runs through Western Power's connection application, coordinated with the retailer:

1. **Confirm the network** — Western Power (SWIS) for Perth and the south-west; Horizon Power for regional/remote WA.
2. **Check the site against export rules** — determine whether the customer will hold a retailer offtake agreement (5kW export) or fall back to 1.5kW.
3. **Lodge the application** — through Western Power's connection process (installers still submit to Western Power, pending a streamlined single-entry process the WA Government is building with Synergy).
4. **Receive approval** — small systems are generally assessed quickly; non-standard systems (over 30kVA aggregate) go through a specialist assessment with fees.
5. **Install and commission** — fit the compliant inverter, set the AS/NZS 4777.2:2020 "Australia Region B" grid code, and complete CSIP-AUS commissioning (Synergy customers).
6. **Set up emergency solar management** — remote disconnect/reconnect capability, or confirm the 1.5kW static export setting.
7. **Lodge the electrical certificate** — under the Electricity (Licensing) Regulations 1991 (WA), administered by Building and Energy.

**Above 30kVA aggregate** the job moves into a non-standard connection process with a technical specialist assessment and connection fees.

---

## Inverter Sizing: The Practical Limits

The 30kVA headline needs translating into per-inverter limits installers actually work with:

| Connection type | Inverter limit |
|---|---|
| Single-phase, single inverter | 10kVA |
| Three-phase, single inverter (large network) | 15kVA |
| Three-phase with a 30kVA inverter | Must be generation-limited to 15kW |
| Aggregate (all inverters, from 1 May 2026) | 30kVA |

**Two phase-balancing gotchas to know:**

- **10kVA single-phase inverter on a three-phase service** — must be generation-limited to **5kW** to prevent neutral voltage rise and phase imbalance.
- **Multiple single-phase inverters on three-phase** — follow AS/NZS 4777.1 Appendix C: up to 5kVA per phase, or larger units with phase-balance protection (21.7A limit between phases).

**The underground-power factor:** much of Perth's newer suburbs run underground power, which generally simplifies connection (no overhead service drop) but can change what's involved in a switchboard or service upgrade — confirm the site's supply type before quoting.

---

## Battery Storage Requirements

Adding a battery brings its own connection and compliance layer — and pairs naturally with WA's emerging VPP programs, since a battery gives the system somewhere useful to send surplus energy when export is limited.

- Battery installations must meet **AS/NZS 5139** (electrical installation safety for battery systems) — see our [AS/NZS 5139 compliance guide](/blog/as-nzs-5139-battery-storage-compliance).
- The WA **Residential Battery Scheme** offers rebates for eligible battery installs and requires specific battery storage capabilities — see [what a battery really costs](/blog/solar-battery-system-cost-australia-2026).
- STC eligibility for the solar component is governed by the **Clean Energy Regulator** under the **Renewable Energy (Electricity) Act 2000** — see the [STC claim process](/blog/stc-claim-process-solar-installers-australia).
- A battery is also the gateway to joining a **virtual power plant** — Western Power is building VPP capability through Project Jupiter, with real fleet coordination targeted for 2026–2027.

---

## EV Charger Installation Requirements

EV chargers pull meaningful load and increasingly trigger distributor sign-off:

- **Residential:** confirm the existing supply and switchboard can handle the additional load; smart chargers are generally preferred for network visibility.
- **Commercial:** load assessments and capacity upgrades usually apply — see the [commercial EV charging guide](/blog/commercial-ev-charging-installation-guide-electricians) and the [EV charger business case](/blog/ev-charger-installation-electricians-australia-2026).
- The same Western Power connection framework manages new loads and capacity enquiries.

---

## New Connections, Service Upgrades & Switchboards

Beyond solar, Western Power handles the full connection range:

- **New homes and subdivisions** — new connections and temporary builder's supplies
- **Service upgrades** — consumer mains, switchboard, and three-phase upgrades
- **Capacity increases** — when demand (EV chargers, heat pumps, growth) outgrows the existing supply

The discipline is identical to solar: confirm the network constraints and Western Power requirements *before* quoting, because an upgrade that needs a line or transformer study is a different job to a switchboard swap.

---

## Approval Timeframes (What to Tell Your Customer)

| Application type | Typical timeframe |
|---|---|
| Small solar system, standard connection | Generally quick assessment |
| System with remote disconnect (DEBS/offtake) | Standard assessment, coordinated with the retailer |
| Non-standard (>30kVA aggregate) | Longer — specialist assessment, fees apply |
| New connection / service upgrade | Site-specific |

Timeframes move with network workload — always confirm the current expectation through the connection process rather than quoting a fixed number from memory.

---

## Common Mistakes That Get Applications Knocked Back

- **Wrong network** — quoting Western Power for a Horizon Power regional site (or vice versa).
- **Quoting 5kW/phase** — WA export is a nett site total (5kW max), not per-phase like NSW/QLD.
- **Missing the 1.5kW trap** — promising full export on a site with no retailer offtake agreement or no stable internet.
- **Skipping remote disconnect** — installing a post-1 May 2026 system without emergency solar management capability (and no 1.5kW fallback election).
- **Wrong grid code** — not setting AS/NZS 4777.2:2020 "Australia Region B" at commissioning.
- **Phase imbalance** — installing a 10kVA single-phase inverter on a three-phase service without generation-limiting to 5kW.
- **Missing the compliance certificate** — the connection approval doesn't replace the certificate of compliance under the Electricity (Licensing) Regulations 1991 (WA).

---

## How ServiceM8 Manages the WA Connection Job

Every WA connection is a multi-step job with distributor paperwork, an approval trail, and a compliance certificate at the end — exactly what job-management software is built to handle.

A typical solar connection in ServiceM8 runs:

**Lead → Site visit → Quote → Network check → Western Power application → Approval tracking → Install → Commission & CSIP-AUS setup → Compliance certificate → Invoice**

ServiceM8 lets you attach the Western Power approval, track the application against the job, store the compliance certificate and photos, and fire the invoice the moment the job closes — so the paperwork doesn't lag the installation. See [ServiceM8 for solar installers](/blog/servicem8-for-solar-installers), and keep the [solar compliance checklist](/blog/solar-compliance-checklist-2026) and [WA electrical contractor licence guide](/blog/wa-electrical-contractor-licence-guide-2026) close to hand.

---

## The 30-Second Summary

- **One distributor, isolated grid:** Western Power runs the SWIS — not part of the NEM, which drives WA's stricter export rules.
- **Export is nett, not per-phase:** 5kW maximum site export (with a retailer offtake agreement), 1.5kW static fallback without one.
- **1 May 2026 change:** 30kVA aggregate inverter limit, plus remote disconnect (emergency solar management) or a 1.5kW export cap.
- **CSIP-AUS, not SEP2:** WA commissions with CSIP-AUS (like SA), unlike QLD's SEP2.
- **AS/NZS 4777.2:2020 "Australia Region B"** — WA's grid code, differing from the NEM states' 2024 standard.
- **The compliance certificate under the Electricity (Licensing) Regulations 1991 (WA) is separate** from the Western Power connection approval.

## Other State Grid Connection Guides

Installing across the border? Each state has its own distributor framework, export limits and compliance certificate:

- [SA Power Networks guide](/blog/sa-power-networks-solar-connection-guide-2026) — flexible exports mandatory since 1 Jul 2023
- [NSW distributors guide](/blog/nsw-electricity-distributors-solar-connection-guide-2026) — three networks (Ausgrid, Endeavour, Essential), three export limits
- [QLD Energex & Ergon guide](/blog/qld-energex-ergon-solar-connection-guide-2026) — dynamic connections on IEEE 2030.5 SEP2
- [VIC distributors guide](/blog/vic-solar-connection-guide-2026) — five networks, uniform 5kW limit
