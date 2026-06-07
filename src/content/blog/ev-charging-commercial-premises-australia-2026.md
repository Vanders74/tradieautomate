---
title: "EV Charging at Commercial Premises Australia 2026: What Electricians Need to Know"
description: "The complete guide for Australian electricians installing EV charging infrastructure at commercial premises — AS/NZS 3000 compliance, load management, metering, network approvals, and how to price and win commercial EV charging jobs."
pubDate: 'Jun 9 2026'
category: "Solar & Battery"
heroImage: '/hero-ev-charging-commercial-premises-2026.jpg'
tags: ['EV charging', 'commercial', 'electrician', 'EVSE', 'AS/NZS 3000', 'compliance', 'load management']
---

Commercial EV charging is moving from a niche add-on to a mainstream building infrastructure requirement. In 2026, Australian businesses — from office parks to retail centres, industrial estates to hotel chains — are under increasing pressure to provide EV charging for staff, fleet vehicles, and customers. And that means work for electricians.

For solar and electrical contractors already doing commercial work, EV charging infrastructure is the logical next revenue line. But commercial EV charging is materially more complex than residential EVSE installation. Load management, sub-metering, network authority requirements, tenancy billing, and switchboard capacity planning all come into play.

This guide covers what Australian electricians need to know to work in commercial EV charging in 2026: compliance requirements, technical considerations, commercial structures, and how to price the work.

---

## Why Commercial EV Charging Is Different From Residential

Residential EV charger installation is typically straightforward: a dedicated 7.2–22kW circuit from the switchboard, a wall-mounted EVSE unit, a compliance certificate. One charger, one customer, one meter.

Commercial EV charging involves:

- **Multiple chargers** — anywhere from 4 to 100+ charge points on a single site
- **Shared electrical infrastructure** — chargers must fit within the building's existing or upgraded maximum demand
- **Multiple users and billing** — staff, visitors, tenants, or customers each using chargers who may pay per session
- **Network connectivity** — most commercial chargers are networked, requiring integration with a charge point management system (CPMS)
- **Long-term infrastructure planning** — the first 4 chargers might be the foundation for 40 more in three years
- **Regulatory complexity** — network authority approvals, sub-metering requirements, and tenancy legislation all intersect

Getting commercial EV charging right requires a systems-thinking approach, not a residential-job mindset.

---

## Technical Compliance Requirements

### AS/NZS 3000:2018 (Wiring Rules)

All EV charging installations in Australia must comply with AS/NZS 3000:2018 — the Australian and New Zealand Wiring Rules. Key requirements relevant to commercial EVSE:

**Circuit protection:** Each EV charger circuit requires appropriately rated overcurrent protection. The circuit breaker rating must be matched to the charger's continuous load — typically a breaker rated at 125% of the charger's rated current.

**Cable sizing:** Commercial charger circuits carry significant sustained loads. Cable sizing must account for continuous duty (EV chargers are considered continuous load devices), derating for grouping and installation method, and voltage drop over longer cable runs — particularly relevant in large car parks with long cable runs from the switchboard.

**Earthing and RCD protection:** AS/NZS 3000 requires RCD protection for EV charger circuits. For three-phase AC chargers, this typically means Type A or Type B RCDs depending on the charger type and DC fault current characteristics. Many European-origin chargers inject DC components that require Type B RCDs — check manufacturer specifications carefully.

**Switchboard capacity:** Commercial sites often don't have headroom in their existing switchboard. You'll need to assess Maximum Demand, available switchboard capacity, and whether a new switchboard section or network upgrade is required.

### AS/NZS 61851 (EV Charging Equipment)

The EVSE equipment itself must comply with AS/NZS 61851 (Electric Vehicle Conductive Charging Systems). In practice, this means specifying EV chargers from reputable manufacturers with Australian SAA/RCM certification. Don't install uncertified EVSE equipment — it's a compliance breach and creates significant liability exposure.

---

## Load Management: The Critical Design Challenge

The number one technical challenge in commercial EV charging is load management. If 20 vehicles all charge simultaneously at 22kW, that's 440kW of load. Most commercial premises can't absorb that on top of existing building load.

### Dynamic Load Management (DLM)

Dynamic Load Management is the solution. A DLM system monitors the building's total electrical load in real time and allocates available capacity to EV chargers dynamically. When building load is high (peak business hours), charger output is throttled. When building load drops (overnight), charger output ramps up.

DLM requires:
- A smart EVSE system capable of receiving and responding to load management signals
- A building energy management interface or dedicated sub-meter monitoring the switchboard
- A charge point management system (CPMS) that ties it together

As the installing electrician, your role is the electrical infrastructure design and installation. But you need to understand how DLM works to specify the right charger hardware and commission it correctly.

### Maximum Demand and Network Capacity

Before designing a commercial EV charging system, you need to understand:

1. **Existing Maximum Demand** — What is the site's current approved maximum demand from the network authority?
2. **Available headroom** — How much of that demand is already used by building loads?
3. **Future growth** — What's the planned EV charging rollout? Design for phase 2 and 3 now.

If the proposed EV charging load exceeds the site's available headroom, a **network augmentation** (supply upgrade) is required. This is a significant project — involving the network authority, potentially new transformers, HV work, and long lead times (6–18 months in some areas). Identify this early in the project scoping process.

---

## Sub-Metering and Tenant Billing

In commercial buildings with multiple tenants — office parks, strata industrial, retail centres, mixed-use developments — EV charging raises a billing question: who pays for the electricity?

### Options:
**Building owner pays, charging is free to users.** Simple, no metering required, but the building owner absorbs the cost. Common in staff car parks as an employee benefit, but not scalable as numbers grow.

**Per-session billing via the CPMS.** The charge point management system records energy delivered per session and invoices users. Requires networked chargers with user authentication (RFID card, app, or credit card payment at the terminal). Sub-metering is built into the charger; the CPMS handles billing.

**Landlord sub-meters the EV charging circuit and bills tenants.** A separate meter (National Meter Identifier/NMI) for the EV charging infrastructure, with the landlord purchasing electricity at their rate and on-selling it to tenants or users. Requires a separate meter installation and potentially a retail licence depending on the structure — seek legal advice on the on-selling model.

Your job is the electrical installation. But the billing model chosen by the building owner directly affects what you need to install. Clarify the billing model before finalising your design.

---

## AC vs DC Charging for Commercial Sites

### AC Chargers (Level 2, 7–22kW)

The workhorse of commercial EV charging. A 22kW AC charger (three-phase, 32A) can charge most EVs from near-empty to full overnight. In a destination charging context (workplace, shopping centre) where vehicles dwell for several hours, 7–11kW AC chargers are often sufficient.

AC chargers are:
- Relatively low cost ($800–$4,000 per unit for commercial-grade hardware)
- Simple to install (standard AC distribution circuit)
- Suitable for slow and medium charging in dwell-time applications
- The right choice for most car park, workplace, and retail applications

### DC Fast Chargers (50–400kW)

DC fast chargers bypass the vehicle's onboard AC charger and charge the battery directly at high DC current. They can charge most EVs to 80% in 20–45 minutes.

DC fast chargers are:
- High cost ($25,000–$200,000+ per unit)
- Require significant electrical infrastructure (dedicated HV connection for high-power units)
- Appropriate for service stations, highways, fleet depot applications
- Typically outside the scope of standard electrical contractors without specialist DC charging training

For most commercial premises installations (workplaces, retail, hospitality), AC chargers are the right answer. Don't overspec the system — a car park full of 7kW AC chargers connected to a well-designed DLM system is often more practical and cost-effective than a handful of DC chargers.

---

## Network Authority Approvals

Commercial EV charging installations often require engagement with the distribution network authority. Requirements vary by network and by the scale of the installation:

**Small installations (single charger, <20A additional load):** In most cases, no formal network approval is required beyond standard installation and compliance certificate processes.

**Medium installations (multiple chargers, significant additional load):** Formal Maximum Demand application may be required. The network authority needs to confirm the site's supply can accommodate the additional load.

**Large installations (high-power multi-charger sites, 50kW+ total EVSE load):** Network augmentation assessment. May require a new service, transformer upgrade, or substations. Engage the network authority early — approval and works can take 6–18 months.

In practice, get in the habit of checking Maximum Demand for every commercial EVSE job. It takes 30 minutes and can save you from a nasty surprise three months into a project.

---

## How to Price Commercial EV Charging Jobs

Commercial EV charging is not a commodity. The pricing reflects design, coordination, compliance, and commissioning complexity — not just cable and labour.

**Key cost components:**
- EVSE hardware (AC charger units — typically $800–$4,000 per charger)
- Sub-board installation / switchboard modification
- Cable and conduit (can be significant in large car parks)
- Sub-metering hardware and installation
- Network authority application fees (if required)
- CPMS integration and commissioning
- Compliance certificates
- Project management and design

**Typical job values:**
- 4-charger workplace install: $12,000–$35,000
- 20-charger commercial car park: $60,000–$180,000
- 50+ charger large site with DLM and CPMS: $200,000–$500,000+

Margin on EV charging jobs should be higher than residential — the design complexity, coordination, and warranty exposure justify it. Don't race to the bottom on price; the customers who want the cheapest quote are also the customers who create the most warranty headaches.

---

## Building Commercial EV Charging Into Your Business

For solar and electrical contractors looking to build a commercial EV charging practice:

1. **Get trained.** Complete EVSE-specific training (several RTOs offer commercial EV charging installation courses). Some major EVSE brands run installer accreditation programs.

2. **Choose your CPMS partner.** The charge point management system is often the commercial customer's key concern — uptime, reporting, billing, and support. Align with one or two reputable CPMS providers and become a competent installer of their systems.

3. **Build a commercial estimating template.** Commercial EV charging quotes are complex. A structured estimating template that covers all cost components prevents margin leakage.

4. **Start with 4–10 charger jobs.** Develop your workflow and commissioning competency on manageable commercial jobs before tendering for 50+ charger sites.

---

*Related reading: [EV Charger Installation for Electricians Australia 2026](/blog/ev-charger-installation-electricians-australia-2026) · [How to Win Commercial Solar Contracts Australia](/blog/how-to-win-commercial-solar-contracts-australia) · [Scaling Your Solar Electrical Business](/blog/scaling-solar-electrical-business-hiring-growth)*
