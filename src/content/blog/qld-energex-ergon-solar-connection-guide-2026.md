---
title: 'QLD Solar Connection: Energex & Ergon Energy Export Limits, Dynamic Connections & Process'
description: "Connect solar in QLD via Energex or Ergon Energy — 5kW fixed export vs up to 10kW per phase dynamic, application steps, fees and timeframes."
pubDate: 'Aug 31 2026'
updatedDate: 'Aug 31 2026'
category: "Grid Connection"
heroImage: '/hero-qld-energex-ergon-solar-connection-guide-2026.jpg'
faq:
  - question: "Which electricity distributors cover Queensland?"
    answer: "Queensland has two electricity distributors, both owned by Energy Queensland: Energex covers South East Queensland (Brisbane, Gold Coast, Sunshine Coast, Ipswich, Toowoomba), and Ergon Energy Network covers regional and rural Queensland (Cairns, Townsville, Mackay, Rockhampton, Mount Isa, and the rest of the state). Powerlink operates the high-voltage transmission network above both."
  - question: "What are the solar export limits in Queensland?"
    answer: "On a basic (fixed) connection, the export limit is 5kW per phase, with an inverter limit of 10kVA per phase (single-phase) or 30kVA (three-phase). On a dynamic connection, you can export up to 10kW per phase. Premises on the regional single-wire (SWER) network are capped at 2kW per phase. In areas with high solar saturation, a basic connection may be limited to 1.5kVA or zero export."
  - question: "What is a dynamic connection in Queensland?"
    answer: "A dynamic connection (Queensland's term for flexible exports) lets your export limit vary with live network conditions instead of being fixed. The network communicates with your inverter every 5 minutes using the IEEE 2030.5 Smart Energy Profile 2.0 (SEP2) protocol, sending Dynamic Operating Envelopes that allow up to 10kW export per phase. You are always allowed to export at least 1.5kW unless there is a grid emergency."
  - question: "Are dynamic connections mandatory for new solar in Queensland?"
    answer: "No. Unlike South Australia (where flexible exports have been mandatory since 1 July 2023), dynamic connections in Queensland are optional and offered as a negotiated connection. You can still apply for a standard fixed-export connection. Dynamic connections are recommended where you want higher export limits or a larger system without upgrading to three-phase."
  - question: "What protocol does Queensland use — CSIP-AUS or SEP2?"
    answer: "Queensland uses IEEE 2030.5 Smart Energy Profile 2.0 (SEP2), chosen by Energex and Ergon Energy Network after industry consultation in 2020–21. This is closely related to CSIP-AUS (SA HB 218 Common Smart Inverter Profile — Australia), which formalises a nationally consistent interpretation of the same standard. A CSIP-AUS-compliant inverter should be able to be listed as compliant for the Queensland implementation."
  - question: "How long does a QLD solar connection take?"
    answer: "A basic fixed-export application for a small system is generally assessed quickly through the Electrical Partners Portal. A dynamic connection application is a negotiated connection — Energex and Ergon aim to issue a connection offer within 65 business days, and you have 20 business days to accept it. Larger systems and sites with network constraints take longer."
  - question: "Can I install a larger system with a dynamic connection?"
    answer: "Yes. On single-phase, a dynamic connection allows a combined solar and battery system up to 20kVA — up to 10kVA solar inverter plus 10kVA battery inverter capacity — without upgrading to three-phase. A fixed connection would require a three-phase upgrade to reach that size. Note a hybrid inverter on single-phase is capped at 10kVA total combined capacity."
  - question: "Do I need a Certificate of Compliance for a QLD solar installation?"
    answer: "Yes. Electrical work in Queensland is regulated under the Electrical Safety Act 2002 (Qld), administered by the Electrical Safety Office. The licensed electrical contractor must provide the required Certificate of Testing and Compliance (eCoC) for the installation. The distributor connection approval is separate from the electrical compliance certificate — both are required."
---

Connecting solar in Queensland means working with one of two electricity distributors — **Energex** (South East Queensland) or **Ergon Energy Network** (regional and rural Queensland) — and getting the export limit right the first time. Queensland's network already runs one of the highest solar penetration rates in the world, so in many areas a standard fixed-export connection is capped at **5kW per phase**, while a **dynamic connection** unlocks up to **10kW per phase**.

**Queensland has two electricity distributors, both owned by Energy Queensland: Energex covers South East Queensland (Brisbane, Gold Coast, Sunshine Coast, Ipswich, Toowoomba), and Ergon Energy Network covers regional and rural Queensland.** The distributor — not your retailer — approves the connection and sets the export limit. Queensland's point of difference from South Australia and New South Wales is its **dynamic connections**: an optional, negotiated connection that uses the **IEEE 2030.5 SEP2** protocol to let exports rise to 10kW per phase when the network can handle it.

This guide covers both distributors: their coverage, the fixed-vs-dynamic export limits, the application process, battery and EV requirements, approval timeframes, and the mistakes that get applications knocked back.

---

## Who Covers What: The QLD Distributor Map

Queensland's grid is a three-tier structure, and the distributor layer is where your connection gets approved.

| Layer | Company | What they do |
|---|---|---|
| Transmission | Powerlink | High-voltage network (the "motorway") |
| **Distribution** | **Energex / Ergon Energy Network** | Poles, wires, substations — **approve connections and set export limits** |
| Retailer | AGL, Origin, Ergon Retail, etc. | Billing and feed-in tariff — separate from the distributor |

**Distributor coverage lookup:**

| Area | Distributor |
|---|---|
| Brisbane, Ipswich, Toowoomba | Energex |
| Gold Coast, Sunshine Coast | Energex |
| South East Queensland (SEQ) | Energex |
| Cairns, Townsville, Mackay, Rockhampton | Ergon Energy Network |
| Mount Isa, Longreach, rural & remote QLD | Ergon Energy Network |

**The practical upside:** unlike NSW, where three distributors apply three different export limits, Queensland's two distributors are both Energy Queensland subsidiaries and apply the **same connection standards and export limits**. Identify the right distributor from the customer's bill or a postcode lookup, but the rules don't change once you do.

---

## Export Limits: Fixed vs Dynamic (The Section That Wins the Job)

This is the single most important thing to get right when quoting a Queensland solar system — and where the "5kW vs 10kW" decision changes the whole quote.

Queensland offers two export connection options:

| Option | Export limit | Inverter limit | How it works |
|---|---|---|---|
| **Basic (fixed) connection** | **5kW per phase** (2kW SWER) | 10kVA per phase single / 30kVA three-phase | A permanent, fixed cap all year round |
| **Dynamic connection** | Up to **10kW per phase** | 10kVA solar + 10kVA battery (single-phase, 20kVA total) | Export limit varies with live network capacity |

**The per-phase distinction matters.** On a three-phase connection the export limit applies to *each* phase — so a three-phase basic connection exports 15kW total (5kW × 3), while a single-phase basic connection is capped at 5kW regardless of system size.

**The dynamic connection is the key upgrade.** A dynamic connection lets you export up to **10kW per phase** — double the fixed limit — and install a larger system on single-phase:

- **Single-phase dynamic:** up to **20kVA** total — 10kVA solar inverter plus 10kVA battery inverter — without upgrading to three-phase (a fixed connection would require the upgrade).
- **Hybrid inverter on single-phase:** capped at **10kVA total** combined solar + battery capacity.
- **Minimum export:** even when the network needs to restrict exports, you're still allowed **1.5kW** unless there's a significant emergency requiring all generation to stop.

**How it works:** the network communicates with your system every **5 minutes** via Wi-Fi or hard-wired internet using Dynamic Operating Envelopes (DOE). If the connection to the utility server is lost, the system defaults to a 1.5kW export limit after about a day — so a reliable internet connection is part of the job.

**Two edge cases to know before quoting:**

- **SWER lines (regional single-wire):** export is capped at **2kW per phase** on a basic connection, and dynamic connections offer less benefit on SWER. Check the STNW3510 standard for SWER-specific dynamic limits before promising 10kW.
- **High solar saturation areas:** in neighbourhoods already packed with rooftop solar, a basic connection may be assessed at **1.5kVA or zero export**. Use Energex's **Network Capacity Map** to check a site's likely export restriction *before* submitting the application — it shows local generation density and network capacity.

Export limits move — always confirm the current figure in the distributor's portal or the **STNW3510 Dynamic Standard for Small IES Connections** before quoting, not from memory.

---

## Dynamic Connections & Flexible Exports: QLD's Protocol

Queensland uses a different communication protocol from South Australia, and it's worth understanding the distinction.

- Queensland's dynamic connections run on **IEEE 2030.5 Smart Energy Profile 2.0 (SEP2)**, chosen by Energex and Ergon Energy Network after industry consultation in 2020–21.
- This is closely related to **CSIP-AUS** (SA HB 218 Common Smart Inverter Profile — Australia), which formalises a nationally consistent interpretation of the same standard. A CSIP-AUS-compliant inverter should be listable for the Queensland implementation — see our [CSIP-AUS and the 1.5kW export limit explainer](/blog/csip-aus-export-limit-1-5kw-solar).
- Unlike South Australia, dynamic connections are **not mandatory** in Queensland — they're a negotiated connection you opt into.

**The commercial hook:** dynamic connections are Queensland's answer to solar saturation. Instead of rejecting applications in full suburbs (zero export), the network lets you connect a *larger* system and export *more* — just not at full tilt every minute of every day. For an installer, that means you can still sell a 13kW system in a saturated area, whereas a basic connection might cap the customer at 1.5kW or nothing.

Inverters must meet the grid-connection standards **AS/NZS 4777.1:2024** (installation) and **AS/NZS 4777.2:2024** (inverter product requirements), and be on the **Clean Energy Council's** approved products list.

---

## The Solar Connection Process

The process runs through Energy Queensland's **Electrical Partners Portal**, which covers both Energex and Ergon Energy Network:

1. **Check the site first** — use the Network Capacity Map to gauge likely export restrictions before you quote.
2. **Lodge the application** — through the Electrical Partners Portal with the NMI, meter number, and system details.
3. **Choose fixed or dynamic** — apply for a basic connection and see the assessment, or request a dynamic connection up front.
4. **Receive the offer** — a basic connection is assessed quickly; a dynamic connection is a negotiated offer (aimed at within 65 business days).
5. **Accept the offer** — you have 20 business days to accept a dynamic connection offer on the customer's behalf.
6. **Install and commission** — fit the compliant inverter or gateway device and complete the dynamic commissioning process.
7. **Provide SEP2 details** — for a dynamic connection, enter or update the Smart Energy Profile (SEP2) details in the application.
8. **Lodge the electrical certificate** — the eCoC under the Electrical Safety Act 2002 (Qld) is separate from the connection approval.

**Above 30kVA** the job moves into the larger-systems process (up to 1,500kVA under the low-voltage embedded-generation standard). Most residential and small-commercial work sits well under 30kVA.

**Dynamic connection application fee:** $286.62 (excl GST) for systems up to 30kVA from 1 July 2026 — confirm the current fee in the Connections Fees and Charges sheet.

---

## Battery Storage Requirements

Adding a battery brings its own connection and compliance layer — and pairs naturally with a dynamic connection, since surplus energy that can't be exported can charge the battery instead.

- Battery installations must meet **AS/NZS 5139** (electrical installation safety for battery systems) — see our [AS/NZS 5139 compliance guide](/blog/as-nzs-5139-battery-storage-compliance).
- Under a dynamic connection, a **DC-coupled battery only** (or upgrading by only adding a DC battery) does not impact your export capacity.
- STC eligibility for the solar component is governed by the **Clean Energy Regulator** under the **Renewable Energy (Electricity) Act 2000** — see the [STC claim process](/blog/stc-claim-process-solar-installers-australia).
- For what a battery really costs the customer, see [what a battery really costs in Australia](/blog/solar-battery-system-cost-australia-2026).

---

## EV Charger Installation Requirements

EV chargers pull meaningful load and increasingly trigger distributor sign-off:

- **Residential:** confirm the existing supply and switchboard can handle the additional load; smart chargers are generally preferred for network visibility.
- **Commercial:** load assessments and capacity upgrades usually apply — see the [commercial EV charging guide](/blog/commercial-ev-charging-installation-guide-electricians) and the [EV charger business case](/blog/ev-charger-installation-electricians-australia-2026).
- Dynamic connections support EV chargers as part of a compliant DER system, and certified AC EV chargers may be added as dynamic loads in future.

---

## New Connections, Service Upgrades & Switchboards

Beyond solar, the same distributors handle the full connection range:

- **New homes and subdivisions** — new connections and temporary builder's supplies
- **Service upgrades** — consumer mains, switchboard, and three-phase upgrades
- **Capacity increases** — when demand (EV chargers, heat pumps, growth) outgrows the existing supply

The discipline is identical to solar: confirm the network constraints and distributor requirements *before* quoting, because an upgrade that needs a line or transformer study is a different job to a switchboard swap.

---

## Approval Timeframes (What to Tell Your Customer)

| Application type | Typical timeframe |
|---|---|
| Basic fixed-export, small system | Quick assessment via the Portal |
| Dynamic connection offer | Aimed at within 65 business days (20 days to accept) |
| Site with network constraints / high saturation | Longer — may require a network study (fee applies) |
| Larger systems (>30kVA) | Site-specific, longer |
| New connection / service upgrade | Site-specific |

Timeframes for review-queue items move with network workload — always confirm the current expectation in the Portal rather than quoting a fixed number from memory.

---

## Common Mistakes That Get Applications Knocked Back

- **Wrong distributor** — lodging with Energex when the site is Ergon (or vice versa); confirm via the customer's bill.
- **Quoting 10kW export on a basic connection** — the fixed limit is 5kW per phase (2kW on SWER); 10kW needs a dynamic connection.
- **Assuming a saturated area can export** — failing to check the Network Capacity Map and quoting a system the network will cap at 1.5kVA or zero.
- **Non-compliant inverter** — not on the CEC approved list, or not SEP2/CSIP-AUS capable for a dynamic connection.
- **Skipping SEP2 details** — installing a dynamic system without registering the SEP2 device details in the application.
- **Missing the eCoC** — the connection approval doesn't replace the electrical Certificate of Testing and Compliance under the Electrical Safety Act 2002 (Qld).
- **Overpromising on SWER** — promising a 10kW dynamic export on a regional single-wire line that's capped at 2kW.

---

## How ServiceM8 Manages the QLD Connection Job

Every QLD connection is a multi-step job with distributor paperwork, an approval trail, and a compliance certificate at the end — exactly what job-management software is built to handle.

A typical solar connection in ServiceM8 runs:

**Lead → Site visit → Quote → Network capacity check → Distributor application → Approval tracking → Install → Commission & SEP2 registration → eCoC → Invoice**

ServiceM8 lets you attach the distributor offer, track the application against the job, store the eCoC and compliance photos, and fire the invoice the moment the job closes — so the paperwork doesn't lag the installation. See [ServiceM8 for solar installers](/blog/servicem8-for-solar-installers), and keep the [solar compliance checklist](/blog/solar-compliance-checklist-2026) and [QLD electrical contractor licence guide](/blog/qld-electrical-contractor-licence-guide-2026) close to hand.

---

## The 30-Second Summary

- **Two distributors, one standard:** Energex (SEQ) and Ergon Energy Network (regional) are both Energy Queensland and apply the same export limits.
- **5kW fixed vs 10kW dynamic:** a basic connection exports 5kW per phase (2kW SWER); a dynamic connection unlocks up to 10kW per phase.
- **Dynamic connections are optional and negotiated** — Queensland's flexible-export option, running on IEEE 2030.5 SEP2, not mandatory like SA.
- **Single-phase dynamic allows up to 20kVA** (10kW solar + 10kW battery) without a three-phase upgrade.
- **Check the Network Capacity Map before quoting** — saturated areas can be capped at 1.5kVA or zero on a basic connection.
- **The eCoC under the Electrical Safety Act 2002 (Qld) is separate** from the distributor connection approval.

## Other State Grid Connection Guides

Installing across the border? Each state has its own distributor framework, export limits and compliance certificate:

- [SA Power Networks guide](/blog/sa-power-networks-solar-connection-guide-2026) — flexible exports mandatory since 1 Jul 2023
- [NSW distributors guide](/blog/nsw-electricity-distributors-solar-connection-guide-2026) — three networks (Ausgrid, Endeavour, Essential), three export limits
- [WA Western Power guide](/blog/wa-western-power-solar-connection-guide-2026) — isolated SWIS grid, 30kVA aggregate inverter rule
- [VIC distributors guide](/blog/vic-solar-connection-guide-2026) — five networks, uniform 5kW limit
