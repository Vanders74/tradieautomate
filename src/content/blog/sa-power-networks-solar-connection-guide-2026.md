---
title: 'SA Power Networks Solar Connection: Process, Export Limits & Flexible Exports'
description: "How to get solar connected and approved through SA Power Networks — the SEG application (up to 30kVA), 1.5–10kW flexible export limits, CSIP-AUS rules, and timeframes."
pubDate: 'Aug 29 2026'
updatedDate: 'Aug 29 2026'
category: "Solar"
heroImage: '/hero-sa-power-networks-solar-connection-guide-2026.jpg'
faq:
  - question: "Who is the electricity distributor in South Australia?"
    answer: "SA Power Networks (SAPN) is the sole electricity distributor for all of South Australia. ElectraNet operates the high-voltage transmission network, but SAPN owns and operates the distribution network (poles, wires, substations) that every residential and business solar system connects to. Your electricity retailer (AGL, Origin, EnergyAustralia, etc.) is separate from the distributor."
  - question: "What is the solar connection process with SA Power Networks?"
    answer: "For inverters up to 30kVA total (small embedded generation), the process is: submit an application in the SAPN Portal with the NMI and meter number, receive approval (often instant if compliant and no network constraints), install and commission the system, then close out the installation in the Portal. A separate large-embedded-generation process applies above 30kVA."
  - question: "Are flexible exports mandatory for new solar in South Australia?"
    answer: "Yes — since 1 July 2023, all new exporting solar systems in SA must be capable of receiving dynamic export limit commands from SA Power Networks. This means the inverter must support the CSIP-AUS protocol, be internet-connected, and be correctly commissioned. Flexible Exports itself is the connection option that lets the export limit vary between 1.5kW and 10kW per phase."
  - question: "How long does SAPN solar approval take?"
    answer: "For compliant small embedded generation (≤30kVA) with no known network constraints, SAPN applications are auto-approved essentially instantly through the Portal. Sites flagged as Low Hosting Capacity (LHCS) or on SWER lines move to a review queue and may take longer, sometimes requiring a phone call from SAPN's team or a site assessment."
  - question: "Do I still need an eCoC for a solar installation in SA?"
    answer: "Yes. The electronic Certificate of Compliance (eCoC) is a separate, government-regulated document required by the South Australian Office of the Technical Regulator under the Electricity Act 1996 (SA). The SAPN connection approval does not replace the eCoC — both are required."
  - question: "What happens if the inverter loses internet on Flexible Exports?"
    answer: "The system keeps generating, but the export limit reverts to the lower bound (1.5kW per phase for most sites, 0kW for SWER or Low Hosting Capacity sites) until the internet connection is restored. This is why a reliable connection and correct commissioning matter for flexible-export customers."
  - question: "Can I connect a battery with Flexible Exports?"
    answer: "Yes, and it is generally the recommended setup. The battery must meet AS/NZS 5139 electrical installation safety requirements, and it is commissioned alongside the solar inverter. A battery gives the system somewhere useful to send surplus energy when the network temporarily reduces the flexible export limit."
  - question: "What inverter capacity needs a more detailed SAPN assessment?"
    answer: "Small embedded generation covers total inverter capacity up to 30kVA. Above 30kVA, the installation is treated as large embedded generation and goes through a more detailed assessment with additional technical requirements and network studies. Most residential and small-commercial solar sits well within the 30kVA small-embedded-generation band."
---

Connecting a solar system to the grid in South Australia means lodging an application with **SA Power Networks (SAPN)** — the state's single electricity distributor — and getting it approved before the panels go up. For inverters up to 30kVA (small embedded generation), the application is online, and approval is often instant when the system is compliant and there are no known network constraints.

**SA Power Networks (SAPN) is the electricity distributor for all of South Australia** — the company that owns the poles-and-wires network and decides whether your solar system can connect, and how much power it can export. Get the application, the export limit, and the inverter setup right the first time, and the connection is routine; get them wrong and you face rejection, rework, and a delayed invoice.

This guide walks through the full process for electrical contractors and solar installers — the application, flexible exports, battery and EV requirements, approval timeframes, and the mistakes that get applications knocked back.

---

## Who You're Dealing With: SA Power Networks vs Retailer vs Transmission

South Australia has one of the simplest grid structures in the country, which is exactly why this state is a good place to nail the process.

| Layer | Company | What they do |
|---|---|---|
| Transmission | ElectraNet | High-voltage network (the "motorway") |
| **Distribution** | **SA Power Networks (SAPN)** | Poles, wires, substations — **approves your connection and sets export limits** |
| Retailer | AGL, Origin, EnergyAustralia, etc. | Billing and feed-in tariff — separate from the distributor |
| Customer | Your client | The site being connected |

**What this means for installers:** every grid-connected solar, battery, and EV charger job in South Australia goes through SAPN — there's no second distributor to look up. That simplifies quoting, but it also means SAPN's rules are the *only* rules, and they're applied consistently across Adelaide, Mount Gambier, Whyalla, and regional SA.

---

## The Solar Connection Process (Small Embedded Generation, ≤30kVA)

Most residential and small-commercial solar sits in the **small embedded generation (SEG)** band: total inverter capacity of **30kVA or less**. The process runs entirely through the SAPN Portal (`portal.sapowernetworks.com.au`).

1. **Apply online.** Lodge the application in the Portal with the NMI, meter number, and system details.
2. **Receive approval.** Applications are **auto-approved** provided the system meets technical and compliance requirements and the site has no known network constraints. A copy of the approval goes to your customer by email.
3. **Install and commission.** Fit the inverter and any export-limiting or monitoring hardware per the manufacturer's instructions.
4. **Close out in the Portal.** After commissioning, close out the installation to complete the approval requirements.

**Above 30kVA** the job moves into the large embedded generation process, with additional technical requirements and network studies. For the vast majority of trade work, staying under 30kVA keeps the job in the fast, online SEG lane.

---

## Export Limits & Flexible Exports (The Section That Wins the Job)

This is the single most important thing to get right when quoting a South Australian solar system — and it's where most installer mistakes happen.

SA Power Networks offers two export connection options:

| Option | Limit | How it works |
|---|---|---|
| **Fixed export** | 0–1.5kW per phase (varies by area) | A permanent, fixed cap, all year round |
| **Flexible Exports** | 1.5kW up to **10kW per phase** | Export limit adjusts dynamically based on live network capacity |

Flexible Exports uses **internet-connected smart inverters** that receive regular export-limit updates from SAPN and match exports to available grid capacity. For most customers it's a major upgrade over the fixed 1.5kW cap — but it comes with equipment and commissioning requirements.

Inverters must also meet the grid-connection standards: **AS/NZS 4777.1:2024** (installation requirements) and **AS/NZS 4777.2:2024** (inverter product requirements), which Standards Australia updated in August 2024.

**Flexible Exports has been mandatory for new installs since 1 July 2023.** Under the South Australian Government's Dynamic Export Requirements, every new exporting system must be capable of receiving and responding to remote export-limit commands. In practical terms that means:

- A **CSIP-AUS-compliant, internet-connected inverter** (see our [CSIP-AUS and the 1.5kW export limit explainer](/blog/csip-aus-export-limit-1-5kw-solar))
- Correct commissioning and device registration through the inverter manufacturer's app
- Site-wide export control, so any legacy inverters are also brought under the limit

If the inverter loses its internet connection, the system keeps generating but reverts to the lower-bound export limit until the connection returns.

**Two edge cases to know before quoting:**

- **SWER lines (rural SA):** the lower bound is 0kW instead of 1.5kW, and since July 2025 (release TS129) inverter capacity allowances on SWER lines rose from 5kVA to 10kVA. A correctly sized meter isolator is critical.
- **Low Hosting Capacity Sites (LHCS):** a small number of properties are flagged in the Portal with a 0kW lower bound. Selecting Flexible Exports sends the application to "Under Review" for a site assessment.

---

## Battery Storage Requirements

Adding a battery to a South Australian solar job brings its own connection and compliance layer — but it also makes flexible exports more valuable, because surplus energy that can't be exported can charge the battery instead of being curtailed.

- Battery installations must meet **AS/NZS 5139** (electrical installation safety requirements for battery systems) — see our [AS/NZS 5139 compliance guide](/blog/as-nzs-5139-battery-storage-compliance).
- The battery is commissioned alongside the solar inverter to SAPN's requirements.
- STC eligibility for the solar component is governed by the **Clean Energy Regulator** under the **Renewable Energy (Electricity) Act 2000**.
- South Australia also has a state battery rebate — see [SA solar battery rebate 2026](/blog/sa-solar-battery-rebate-2026) and [what a battery really costs](/blog/solar-battery-system-cost-australia-2026).

---

## EV Charger Installation Requirements

EV chargers increasingly trigger their own network considerations, especially as larger home and commercial chargers pull meaningful load.

- **Residential chargers:** confirm the existing supply and switchboard can handle the additional load; smart (internet-connected) chargers are generally preferred for network visibility.
- **Commercial charging:** load assessments and capacity upgrades often apply — see our [commercial EV charging guide](/blog/commercial-ev-charging-installation-guide-electricians) and the [EV charger business case](/blog/ev-charger-installation-electricians-australia-2026).
- The same SAPN Portal is used to manage new loads and connection enquiries.

---

## New Connections, Service Upgrades & Switchboards

Grid connection work isn't just solar. The same SAPN framework covers:

- **New homes and subdivisions** — new connections and temporary builder's supplies
- **Service upgrades** — consumer mains upgrades, switchboard upgrades, and three-phase upgrades
- **Capacity increases** — when a site's demand (EV chargers, heat pumps, a growing business) outgrows its existing supply

The key discipline here is the same as solar: confirm the network constraints *before* quoting, because an upgrade that needs a transformer or line study is a different job to a simple switchboard swap.

---

## Approval Timeframes (What to Tell Your Customer)

Accurate expectations keep customers happy and protect your invoice. These are the practical figures for the SEG process:

| Application type | Typical timeframe |
|---|---|
| Solar PV ≤30kVA (compliant, no constraints) | Instant (auto-approved) |
| Flexible Exports (standard site) | Instant approval, then commissioning + device registration |
| Low Hosting Capacity or SWER site | Review queue — may require a SAPN call or site assessment |
| Large embedded generation (>30kVA) | Site-specific, longer |
| New connection / service upgrade | Site-specific |

Timeframes for review-queue items move as SAPN's workload changes — always confirm the current expectation in the Portal rather than quoting a fixed number from memory.

---

## Common Mistakes That Get Applications Knocked Back

Most rejections are avoidable and come down to the same handful of issues:

- **Incorrect or incomplete applications** — missing NMI, meter number, or customer details
- **Export configuration errors** — inverter not set to the approved export limit, or legacy inverters not brought under site-wide control
- **Non-compliant inverter** — not CSIP-AUS / dynamic-export capable (mandatory since 1 July 2023)
- **Missed device registration** — the inverter was installed but never registered through the manufacturer's app, so SAPN doesn't know it's there
- **Skipping the eCoC** — the connection approval doesn't replace the government-regulated electronic Certificate of Compliance
- **Poor customer expectation management** — quoting flexible exports at a 0kW or Low Hosting Capacity site without checking the Portal first

---

## How ServiceM8 Manages the SAPN Job End-to-End

Every SAPN connection is a multi-step job with documents, approvals, and a compliance trail — which is exactly what job-management software is built to handle.

A typical solar connection in ServiceM8 runs:

**Lead → Site visit → Quote → SAPN application → Approval tracking → Install → Commission & device registration → eCoC → Invoice**

ServiceM8 lets you attach the SAPN approval, track the application status against the job, store the eCoC and compliance photos, and fire the invoice the moment the job closes out — so the paperwork doesn't lag the installation. See [ServiceM8 for solar installers](/blog/servicem8-for-solar-installers) for the full workflow, and keep the [solar compliance checklist](/blog/solar-compliance-checklist-2026) and [STC claim process](/blog/stc-claim-process-solar-installers-australia) close to hand.

---

## The 30-Second Summary

- **One distributor, one process:** SA Power Networks handles every grid connection in South Australia.
- **≤30kVA is the fast lane:** small embedded generation applications are online and often auto-approved.
- **Flexible Exports is mandatory for new installs (since 1 July 2023):** up to 10kW per phase, but it needs a CSIP-AUS, internet-connected inverter with correct commissioning.
- **Know the edge cases before quoting:** SWER (0kW lower bound) and Low Hosting Capacity sites (0kW, review queue).
- **The eCoC and STC compliance are separate obligations** — the SAPN approval doesn't cover them.
