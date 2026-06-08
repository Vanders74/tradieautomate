---
title: "EV Charging at Commercial Premises Australia 2026: What Electricians Need to Know"
description: "The complete guide for Australian electricians installing EV charging infrastructure at commercial premises — AS/NZS 3000 compliance, load management, metering, network approvals, pricing, and how to build commercial EV charging as a revenue line."
pubDate: 'Jun 9 2026'
category: "Solar & Battery"
heroImage: '/hero-ev-charger-installation.jpg'
tags: ['EV charging', 'commercial', 'electrician', 'EVSE', 'AS/NZS 3000', 'compliance', 'load management']
---

Commercial EV charging is moving from a niche add-on to a mainstream building infrastructure requirement. In 2026, Australian businesses — from office parks to retail centres, industrial estates to hotel chains — are under increasing pressure to provide EV charging for staff, fleet vehicles, and customers. Every one of those charge points needs a licensed electrician to install it.

For solar and electrical contractors already working in the commercial space, EV charging infrastructure is a natural next revenue line. But commercial EV charging is materially more complex than a residential EVSE installation. Load management, sub-metering, network authority approvals, switchboard capacity planning, and the interplay with existing solar systems all come into play.

This guide covers what Australian electricians need to know to work in commercial EV charging in 2026: compliance requirements, technical considerations, commercial structures, and how to price and win the work.

---

## Why Commercial EV Charging Is Different From Residential

A residential EV charger installation is typically straightforward — a dedicated 7.2kW circuit from the switchboard, a wall-mounted EVSE, a compliance certificate, a satisfied customer. One charger, one customer, one meter.

Commercial EV charging involves:

- **Multiple chargers** — anywhere from 4 to 100+ charge points on a single site
- **Shared electrical infrastructure** — chargers must fit within the building's existing or upgraded maximum demand
- **Multiple users** — staff, visitors, tenants, or paying customers each using the network
- **Sub-metering and billing** — session-level energy measurement for user billing or cost allocation
- **Network connectivity** — most commercial chargers are networked, requiring integration with a charge point management system (CPMS)
- **Long-term infrastructure planning** — the first 4 chargers are often the foundation for 40 more over the next three years

Getting commercial EV charging right requires a systems-thinking approach. The businesses that do it well are treating commercial EV infrastructure as a deliberate specialisation, not a residential job at larger scale.

---

## Compliance Requirements

### AS/NZS 3000:2018 — Wiring Rules

All EV charging installations must comply with AS/NZS 3000:2018. Key requirements for commercial EVSE:

**Circuit protection:** Each EV charger circuit requires appropriately-rated overcurrent protection. The circuit breaker rating must be sized at 125% of the charger's rated continuous current.

**Cable sizing:** Commercial charger circuits carry significant sustained loads. Cable sizing must account for continuous duty derating, grouping derating, installation method, and voltage drop — particularly relevant in large car parks with long cable runs from the switchboard. Undersized cable is both a compliance failure and a fire risk.

**Earthing and RCD protection:** RCD protection is required for all EV charger circuits. For three-phase AC chargers, the correct RCD type matters — many European-origin chargers produce DC fault current components that require Type B RCDs rather than standard Type A. Check manufacturer specifications before specifying RCDs.

**Switchboard capacity:** Most commercial sites don't have spare headroom in their existing switchboard. Assess available Maximum Demand before quoting.

### AS/NZS 61851 — EV Charging Equipment Standards

EVSE equipment installed in Australia must comply with AS/NZS 61851 (Electric Vehicle Conductive Charging Systems). In practice, specify equipment from reputable manufacturers with Australian SAA/RCM certification. Uncertified imports create compliance liability and may not be covered by your public liability insurance in the event of a fault.

For your own compliance requirements as an electrical contractor in commercial environments, ensure your [electrical contractor insurance](/blog/electrical-contractor-insurance-australia-2026) explicitly covers EV charging installation work — some policies have exclusions or sub-limits for EV infrastructure.

### State Electrical Compliance Certificates

EV charger installation is electrical work and requires the appropriate compliance certificate in each state — Certificate of Compliance Electrical Work (CCEW) in NSW, Certificate of Electrical Safety (CES) in Victoria, Certificate of Testing and Compliance in Queensland, or CCEI in WA. The same process applies as for any commercial electrical installation. For NSW specifically, the [CCEW compliance guide](/blog/ccew-nsw-electrical-compliance-guide-2026) covers the documentation and lodgement requirements in detail.

---

## Load Management: The Critical Design Challenge

The number one technical challenge in commercial EV charging is load management. If 20 vehicles charge simultaneously at 22kW, that's 440kW of additional load. Most commercial premises can't absorb that on top of existing building loads — and the network authority won't approve it without a supply upgrade.

### Dynamic Load Management (DLM)

Dynamic Load Management is the industry solution. A DLM system monitors the building's total electrical load in real time and allocates available capacity to EV chargers dynamically. When building load is high, charger output is throttled back. When building load drops overnight, charger output ramps up.

A well-designed DLM system means a car park with 40 chargers can operate within the same Maximum Demand approval as a site with 10 chargers — because the chargers never all draw full power simultaneously.

DLM requires:
- Smart EVSE hardware capable of receiving and responding to load signals
- A building sub-meter or energy management interface monitoring the switchboard
- A charge point management system (CPMS) tying the load data and charger control together

As the installing electrician, you're responsible for the electrical infrastructure design and installation. But you need to understand DLM well enough to specify compatible hardware and commission the system correctly — selecting an EVSE brand with robust DLM support is a prerequisite for any multi-charger commercial site.

### Maximum Demand and Network Authority Approval

Before designing a commercial EV charging system:

1. **Determine the site's existing Maximum Demand approval** — What has the distribution network authority approved for this site?
2. **Assess available headroom** — How much of that approved demand is already consumed by building loads?
3. **Project EV charging load** — What's the peak concurrent charging load from the proposed charger count? Apply DLM to calculate the actual additional demand required.
4. **Plan for future stages** — Design the electrical infrastructure for Phase 2 and Phase 3 now, even if you're only installing Phase 1 today. Running conduit for future cable capacity costs almost nothing during construction; retrofitting it later costs significantly more.

If the proposed EV charging load exceeds the site's available headroom under DLM, a **network augmentation** — a supply upgrade — is required. This involves the distribution network authority, potentially new transformers or HV equipment, and lead times of 6–18 months in many network areas. Identify this at scoping, not during installation.

---

## Sub-Metering and Billing Models

In commercial buildings with multiple tenants or users, EV charging creates a billing question: who pays for the electricity?

**Three common models:**

**Building owner pays, free to users:** Simple, no session billing required. Common in staff car parks as an employee benefit. Not scalable as EV penetration grows — the electricity cost becomes material.

**Session billing via the CPMS:** The charge point management system records energy delivered per session and invoices users. Requires networked chargers with user authentication — RFID card, mobile app, or tap-to-pay at the terminal. Sub-metering is built into the charger hardware; the CPMS handles billing. This is the most scalable model for large sites.

**Landlord sub-meters and on-sells:** A separate electrical sub-meter (potentially with its own NMI) for the EV charging infrastructure, with the landlord purchasing electricity and on-selling to tenants or users. Requires a separate meter installation — and depending on the structure, may require a retail licence for the on-selling arrangement. Seek legal advice before recommending this model to commercial customers.

Your job is the electrical infrastructure. But the billing model chosen by the building owner directly affects what you install — session billing via CPMS requires different hardware to a "free to staff" model. Clarify the billing intent before finalising your design.

---

## AC vs DC Charging for Commercial Sites

### AC Chargers (Level 2, 7–22kW)

The workhorse of commercial EV charging. A 22kW AC charger (three-phase, 32A) can charge most EVs from near-empty to full overnight. In a destination charging context — workplace, shopping centre, hotel — where vehicles dwell for several hours, 7–11kW AC chargers are often the most practical and cost-effective choice.

AC commercial chargers typically cost $800–$4,000 per unit (hardware only, before installation). They're straightforward to install using standard AC distribution circuits.

### DC Fast Chargers (50–400kW)

DC fast chargers bypass the vehicle's onboard AC charger and charge the battery directly at high DC current. Most EVs can charge from 20%–80% in 20–45 minutes at a 50kW+ DC charger.

DC fast chargers cost $25,000–$200,000+ per unit and require dedicated high-power electrical infrastructure — often including HV connection upgrades. They're appropriate for service stations, highway rest stops, fleet depots, and high-dwell applications.

For most commercial premises (workplaces, retail, hospitality), AC chargers with DLM is the right answer. Don't overspec the system. A car park full of 7kW AC chargers on a well-designed DLM system is more practical, more cost-effective, and easier to maintain than a handful of high-power DC units. See our [EV charger installation guide for electricians](/blog/ev-charger-installation-electricians-australia-2026) for a detailed breakdown of residential vs commercial charging use cases.

---

## Network Authority Approvals

Commercial EV charging often requires formal engagement with the distribution network authority:

| Installation Scale | Approval Likely Required? |
|---|---|
| Single charger, under 20A additional load | Generally no formal approval required |
| Multiple chargers, significant load addition | Maximum Demand application to the DNSP |
| High-power multi-charger site, 50kW+ total | Network augmentation assessment — allow 6–18 months |

Get into the habit of checking Maximum Demand for every commercial EVSE job at the scoping stage. A quick call to the DNSP to confirm available headroom takes 30 minutes and can save you months of delays and a re-scoped project budget.

---

## Pricing Commercial EV Charging Work

Commercial EV charging is not a commodity. The design complexity, coordination, DLM commissioning, and compliance documentation all justify a higher margin than residential installation.

**Key cost components:**

| Component | Typical Range |
|---|---|
| EVSE hardware (AC charger units) | $800–$4,000 per charger |
| Sub-board installation / switchboard modification | $2,000–$8,000+ |
| Cable and conduit (significant in large car parks) | Variable |
| Sub-metering hardware and installation | $500–$2,000 |
| Network authority application fees | Variable |
| CPMS integration and commissioning | $500–$3,000 |
| Compliance certificates | $50–$300 per installation |
| Project management and design | 10–15% of project value |

**Typical project values:**
- 4-charger workplace install: $12,000–$35,000
- 20-charger commercial car park: $60,000–$180,000
- 50+ charger site with DLM and CPMS: $200,000–$500,000+

Use a structured estimating template for commercial EV charging quotes — every cost component above must be captured. The [hidden admin cost calculator](/blog/hidden-admin-cost-calculator) can help you quantify what poor estimating processes cost your business across the year.

---

## Building Commercial EV Charging Into Your Business

For solar and electrical contractors looking to build a commercial EV charging practice:

**Get trained.** Complete EVSE-specific training (several RTOs offer commercial EV installation courses). Major EVSE brands including Wallbox, Zappi, and Tritium run installer accreditation programs — their certified installer networks are often their primary sales channel.

**Choose your CPMS partner.** The charge point management system is often the commercial customer's primary concern — uptime, reporting, billing reliability, and support. Align with one or two reputable CPMS providers and become a competent integrator of their systems.

**Track every job properly.** Commercial EV jobs have longer documentation tails than residential — commissioning records, CPMS integration notes, DLM settings, compliance certificates. Use [ServiceM8](https://www.servicem8.com/?ref=tradieautomate) or equivalent to create a commercial EV job type with its own completion checklist, so nothing gets missed between installation and final invoice.

**Price for complexity.** The contractors who build successful commercial EV practices are the ones who price for the design and commissioning complexity, not just the cable and labour hours. Customers who want the cheapest quote are also the customers who create the most warranty headaches.

---

*This article provides general guidance only. Compliance requirements, network authority rules, and scheme details are subject to change — always verify current requirements with your state electrical regulator and relevant DNSP.*

---

> **Got a compliance or technical question right now?**
> [Ask Tradie Brain AI free →](https://tradieautomate.com/tools/tradie-brain/) Instant answers on AS/NZS 3000, EV charger approvals, network authority requirements, CCEW lodgement, and more. No login required.

---

## Related Reading

- *[EV Charger Installation for Electricians: Certification, Compliance and Workflow in Australia](/blog/ev-charger-installation-electricians-australia-2026)*
- *[How to Win Commercial Solar Contracts in Australia](/blog/how-to-win-commercial-solar-contracts-australia)*
- *[Electrical Contractor Insurance Australia 2026: What Coverage You Actually Need](/blog/electrical-contractor-insurance-australia-2026)*
- *[NSW CCEW Compliance Guide for Electrical Contractors 2026](/blog/ccew-nsw-electrical-compliance-guide-2026)*
- *[Digital Job Management for Solar Installers](/blog/digital-job-management-solar-installers)*
- *[Scaling a Solar and Electrical Business: Hiring, Systems and Growth](/blog/scaling-solar-electrical-business-hiring-growth)*
- *[5 Hidden Costs Killing Your Profit as a Solar Installer or Electrician](/blog/hidden-costs-killing-profit-solar-electrician)*
- *[The Hidden Admin Cost Calculator: What Aussie Tradies Really Lose Each Week](/blog/hidden-admin-cost-calculator)*
