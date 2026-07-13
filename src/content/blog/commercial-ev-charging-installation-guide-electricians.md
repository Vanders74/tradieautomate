---
title: "Commercial EV Charging Installation: The Electrician's Business Guide for 2026"
description: "Commercial EV charging installation guide for Australian electricians — DNSP approvals, load management design, OCPP, quoting multi-site jobs, and how to build a repeatable high-margin EV charging service."
pubDate: 'Jul 13 2026'
category: "Solar & Battery"
heroImage: '/hero-ev-charger-installation.jpg'
tags: ['commercial EV charging', 'EV charger installation', 'EVSE', 'load management', 'OCPP', 'electrician', 'AS/NZS 3000']
---

Residential EV charger installation is a useful entry point. But the real commercial opportunity for Australian electricians in 2026 is commercial EV charging — workplaces, strata buildings, shopping centres, car parks, fleet depots, and hospitality venues. These sites need multiple chargers, professional design, DNSP engagement, and ongoing management. They're not competitive on price the same way residential is. And they're sticky — once you've installed and commissioned a commercial EV charging site, you own the maintenance relationship.

This guide covers the technical, compliance, and business requirements for Australian electricians looking to build commercial EV charging as a genuine service line — not just a one-off job.

---

## The Commercial EV Charging Market in 2026

The numbers are significant. Australia's EV fleet is growing at 30–40% annually. Every employer with a company car policy, every strata building with resident parking, every shopping centre competing for customer dwell time, and every fleet depot with company vehicles is a commercial EV charging opportunity.

What differentiates commercial from residential:

- **Multiple chargers, often networked** — not one charger on one wall
- **Higher power levels** — from 22 kW AC three-phase up to 50–350 kW DC fast charging
- **Load management required** — multiple chargers sharing a limited supply without overwhelming the main switchboard or triggering demand charges
- **DNSP engagement essential** — for any commercial installation above 22 kW aggregate, a formal network application is required
- **OCPP-based management common** — Open Charge Point Protocol allows remote monitoring, user authentication, billing, and load balancing
- **Business case expected** — commercial clients want an ROI analysis and operating cost model, not just an installation quote

---

## Commercial EV Charger Types and Power Levels

Understanding the product options is the starting point for designing commercial sites.

### AC Level 2 (7.2 kW Single-Phase, 22 kW Three-Phase)

The standard for workplace and destination charging. Vehicles left for 4–8 hours can gain 50–150 km of range per session. Costs $800–$4,000 per unit depending on brand and features.

**Best for:** Workplaces, retail car parks, hotels, strata visitor parking. Any site where cars are stationary for 2+ hours.

Key brands in Australia: Ocular, Wallbox, Charge Amps, EVBox, JuiceBox, Tesla Wall Connector (for fleet sites).

### DC Fast Charging (50 kW – 350 kW)

Vehicles gain 100–300 km of range in 20–45 minutes. Significantly higher infrastructure cost: $20,000–$150,000+ per unit plus civil and electrical infrastructure.

**Best for:** Highway corridors, service stations, large shopping centres with high dwell-time throughput goals, government EV hubs. Not typically suitable for standard commercial premises.

For most commercial electrician businesses in 2026, AC Level 2 is the core product. DC fast charging involves higher capital and more complex commissioning — a specialisation for businesses deliberately pursuing that niche.

### AC Three-Phase 22 kW

The high end of AC Level 2. Requires three-phase supply at the site (most commercial premises have this). Compatible vehicles can achieve close to full charge in 2–3 hours, or gain 120–140 km/hour on a capable vehicle.

Not all EVs can charge at the full 22 kW — check vehicle on-board charger ratings. Most current-generation EVs cap at 7–11 kW AC; 22 kW is future-proofing.

---

## Compliance and Standards for Commercial EV Charging

### AS/NZS 3000 — Wiring Rules

All EV charger installation work in Australia must comply with AS/NZS 3000. For commercial sites, the key requirements:

- **Dedicated circuits** — each EV charger requires a dedicated circuit from the switchboard or sub-switchboard with appropriate overcurrent protection
- **RCD protection** — Type A RCDs (minimum) required for EV charging circuits; Type B RCDs required for some DC-leakage-capable chargers (check charger manufacturer specification)
- **Cable sizing** — size for continuous load (EV chargers are long-duration loads — cable must be rated for continuous duty at the charger's rated current)
- **Labelling** — circuit breakers must be labelled for EV charging circuits; hazard labels on the charger where required

### DNSP Notification and Approval

For commercial EV charging above the DNSP's notification threshold (typically 22 kW aggregate), a formal network application is required before installation:

- Submit load details, location, proposed installation date
- The DNSP will assess whether the local network can support the load or whether a network augmentation is required
- Approvals can take 4–12 weeks; factor this into project timelines at the quote stage
- Some DNSPs are actively streamlining this process for commercial EV charging — check your DNSP's published EV charging guide

### EV Charger Standards

Commercial EVSE must comply with IEC 61851 (electric vehicle conductive charging system) and AS/NZS 61851 (the Australian adoption). Chargers sold through reputable distributors are already IEC 61851 compliant; verify this before specifying.

**CSIP-AUS (Common Smart Inverter Profile — Australia):** From 2024, some DNSPs require EV chargers above certain power levels to be CSIP-AUS compatible — allowing the network to curtail charging during peak demand events. Check your DNSP's current requirements.

---

## Load Management Design — The Core Technical Skill

Commercial EV charging sites with multiple chargers need load management to prevent the aggregate EV load from exceeding the site's maximum demand allocation.

### Static Load Limiting

The simplest approach: cap the total available EV charging power at a fixed level, divided equally across connected chargers. If 3 chargers share 21 kW, each gets 7 kW maximum, regardless of how many vehicles are connected.

**Advantage:** Simple, no smart technology required. Works with basic chargers.
**Disadvantage:** Inefficient — if only 1 vehicle is present, it still only charges at 7 kW rather than the full 21 kW.

### Dynamic Load Management (DLM)

Chargers communicate in real time to share available capacity dynamically. If 1 vehicle is charging, it uses up to the full site allocation. As more vehicles connect, the controller reduces each charger's output proportionally.

**Equipment required:** DLM-capable chargers and either a dedicated load management controller or a CPMS (Charge Point Management System) with DLM functionality.

**Advantage:** Significantly more efficient — vehicles charge faster when demand is low.
**Best for:** Any multi-charger commercial site where session count varies throughout the day.

### Building Energy Management Integration

For commercial sites with existing BMS (Building Management Systems), the most sophisticated approach is integrating EV charging load management with the building's overall energy monitoring. This allows the EV charging system to respond to total site demand — reducing EV charging output during periods of high building load to stay within the site's maximum demand cap.

This protects the commercial customer from demand tariff spikes, which in commercial energy contracts can significantly inflate electricity costs.

---

## OCPP — Open Charge Point Protocol

OCPP (Open Charge Point Protocol) is the open standard that allows EV chargers from different manufacturers to communicate with a central Charge Point Management System (CPMS). Specifying OCPP-compliant chargers gives commercial clients the flexibility to:

- Monitor all charging sessions in real time
- Authenticate users (RFID, app-based, QR code)
- Restrict charging to specific users or vehicles
- Charge back to individual employees or fleet vehicles
- Generate energy and cost reports
- Integrate with building management and energy management systems

**OCPP 1.6 vs OCPP 2.0.1:** OCPP 1.6 is the current deployment standard in most commercial installations. OCPP 2.0.1 adds improved security, device management, and smart charging capabilities. Some newer chargers support 2.0.1; confirm with the manufacturer.

**CPMS options for Australian commercial sites:**
- Charge HQ (Australian, popular for SME commercial sites)
- Monta (European, strong OCPP support, growing Australian base)
- EV Connect, ChargePoint Network (US-based, suitable for larger multi-site deployments)
- Manufacturer-provided platforms (Wallbox Optimus, EVBox Everon, etc.)

For most commercial sites up to 20 chargers, the manufacturer's own CPMS or Charge HQ is sufficient. For large multi-site or fleet deployments, a vendor-neutral CPMS gives more flexibility.

---

## Quoting Commercial EV Charging Jobs

A commercial EV charger quote is materially different from a residential quote. The client expects a professional proposal, not a single price line.

**What a commercial EV charging proposal should include:**

**1. Site Assessment Summary**
- Current supply capacity and available headroom
- Sub-switchboard or new switchboard required?
- Cable run lengths and access complexity
- DNSP engagement status (pre-consultation recommended before quoting)

**2. Equipment Specification**
- Charger brand, model, power rating, connector type
- Charge management system or OCPP platform
- Load management approach (static vs DLM)
- Warranty terms

**3. Electrical Design Summary**
- Circuit breaker and cable sizing
- RCD type and installation location
- Sub-board if required
- Load management controller if applicable

**4. Installation Programme**
- Project stages
- DNSP approval timeline (be explicit — this is often the longest lead item)
- Installation and commissioning days required

**5. Cost Breakdown**
- Equipment cost (per charger, CPMS setup, load management hardware)
- Electrical installation (labour, materials, switchboard/sub-board)
- CPMS setup and commissioning
- DNSP application and any network contribution fees

**6. Operating Cost and ROI Model**
Commercial clients expect this. Simple version: annual energy cost per charger, charging session revenue potential (if charging employees or customers), total investment payback.

---

## Building a Recurring Revenue Stream

Commercial EV charging creates ongoing service relationships that residential work rarely does:

**Maintenance contracts.** Chargers need annual inspection, firmware updates, and occasional component replacement. A 12-month maintenance agreement at $200–$500 per charger per year is a reasonable and well-accepted commercial offering.

**CPMS subscription management.** Some installers manage the CPMS subscription on behalf of the client, adding a small margin to the platform cost and providing first-line support. This is low-effort ongoing revenue.

**Upgrade cycles.** Commercial clients will need to expand capacity as EV adoption in their fleet or customer base grows. Your position as the incumbent installer makes you the obvious choice for the expansion — if you've maintained the relationship.

**Reporting and energy management consultation.** As demand tariff exposure becomes a real cost for commercial clients with EV charging loads, the ability to advise on smart charging schedules and demand management becomes a genuine value-add service.

---

## FAQ

### What size supply does a commercial EV charging site need?

It depends on the number of chargers and the load management approach. For 10 × 7.2 kW chargers with static load limiting at 50% utilisation, you'd design for approximately 36 kW of EV load. Add this to the existing site peak demand and confirm the total against the DNSP supply capacity. A site with a 100 kW supply and 60 kW existing peak demand has 40 kW available for EV charging — enough for 5–6 chargers at full AC three-phase without augmentation.

### Do I need a specific licence to install commercial EV chargers?

A standard electrical contractor licence and CEC accreditation (for solar-integrated sites) are the primary requirements. Some states may have additional requirements for high-power DC charging infrastructure. Check with your state electrical safety regulator before tendering for DC fast charging work.

### What is the typical project timeline for a commercial EV charging installation?

Allow 8–14 weeks from confirmed order for most commercial jobs: 2 weeks for equipment procurement, 4–8 weeks for DNSP approval (the most variable element), and 1–3 days for installation and commissioning. Communicate this timeline explicitly in your proposal — commercial clients who expect a 2-week turnaround will be frustrated.

### Can I install EV chargers in a strata car park?

Yes, but strata installations require body corporate approval. The electrical infrastructure serving individual bays may be the owner corporation's responsibility (common property) or the individual owner's (if metered separately). A strata EV charging consultation should address: common property vs lot supply, metering/billing approach, future proofing the infrastructure for multiple residents, and the body corporate's formal approval process.

### What's the difference between a dedicated EV charger and a heavy-duty power outlet?

A dedicated EVSE (Electric Vehicle Supply Equipment) is purpose-designed for EV charging — it includes safety features such as pilot signal communication with the vehicle (which prevents charging unless the vehicle is properly connected), ground fault protection, and thermal management. A heavy-duty outlet (e.g. 32A single-phase industrial socket) lacks these safety features and is not recommended for EV charging. Most EV manufacturers void charging warranties for damage caused by non-EVSE charging sources.

---

## Related Reading

- [Commercial EV Charging at Commercial Premises Australia 2026](/blog/ev-charging-commercial-premises-australia-2026/)
- [EV Charger Installation Cost Australia 2026](/blog/ev-charger-installation-cost-australia-2026/)
- [EV Charger Network Installation: Business Opportunity for Electricians](/blog/ev-charger-network-installation-business-opportunity/)
- [Commercial Solar System Compliance Australia](/blog/commercial-solar-system-compliance-australia/)
- [Electrical Switchboard Upgrade Cost Australia 2026](/blog/electrical-switchboard-upgrade-cost-australia-2026/)
- [Best Job Management Software for Electricians Australia](/blog/best-job-management-software-electricians-australia/)

[Start your free ServiceM8 trial →](https://www.servicem8.com/?ref=tradieautomate)
