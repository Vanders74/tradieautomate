---
title: "3-Phase Power Upgrade Cost Australia 2026: $3K–$10K"
description: "3-phase power upgrade in Australia 2026: $3K–$10K installed, the DNSP application that decides the timeline, and the AS/NZS 3000 rules that get jobs failed."
pubDate: "Aug 2026"
updatedDate: "Oct 19 2026"
category: "Compliance"
breakdown:
  - title: "Assess the load"
    summary: "Maximum demand calc per AS/NZS 3000 Appendix C."
  - title: "Lodge the DNSP application"
    summary: "Before ordering anything — this is the long lead time, not the wiring."
  - title: "Upgrade the switchboard"
    summary: "AS/NZS 3000 Clauses 2.6 + 2.10: RCD on every ≤32A sub-circuit, clearances at 1 m / 600 mm."
    href: "/blog/rcd-safety-switch-requirements-as-nzs-3000-electricians-2026"
    hrefLabel: "RCD requirements →"
  - title: "Level 2 ASP connection"
    summary: "Network-side work needs an authorised provider."
  - title: "Coordinate the meter"
    summary: "Avoid unmetered 3-phase — book the meter near the connection."
  - title: "Test + issue the cert"
    summary: "Section 8 testing, then the certificate — CCEW within 7 days in NSW; in VIC a switchboard change is prescribed, so the COES is signed within 4 business days and notified to ESV within 2 of signing."
    href: "/blog/electrical-switchboard-upgrade-cost-australia-2026"
    hrefLabel: "Switchboard cost guide →"
heroImage: "/hero-3-phase-power-upgrade-guide.jpg"
tags: ["3-phase", "switchboard upgrade", "AS/NZS 3000", "electrical compliance", "power upgrade"]
faq:
  - question: "How much does a 3-phase power upgrade cost in Australia?"
    answer: "A single-phase to 3-phase upgrade in Australia typically runs **$3,000–$10,000**: switchboard replacement $1,500–$4,000, the DNSP connection fee $500–$1,500, cable run $500–$2,000, a three-phase smart meter $300–$700, and Level 2 ASP labour $800–$1,500. The $10,000 end is asbestos-backed boards, long underground runs through concrete, and meter relocations. Western Power publishes $586–$853 for an overhead single-to-three-phase conversion; that's the network side only, not the board."
  - question: "Do I need a 3-phase upgrade for solar or an EV charger?"
    answer: "Usually not for solar alone. Ausgrid and Energex both approve up to 10kW of inverter capacity per phase, so a single-phase home can carry a 10kW inverter without a supply upgrade — 30kW is the three-phase ceiling on the same streamlined approval. Above 10kW per phase in NSW you move to a technical assessment. A 3-phase upgrade is justified when the customer needs more than 10kW of inverter, wants 22kW three-phase EV charging, or already has single-phase loads pressed against a 63A–80A supply. Keep export limits separate from inverter limits: Energex approves a 10kW single-phase inverter to export 5kW."
  - question: "What are the AS/NZS 3000 requirements for a 3-phase switchboard upgrade?"
    answer: "Clause 2.6 requires 30mA RCD protection on all final sub-circuits in domestic installations (2.6.3.2.2), and 2.6.3.2.5 requires RCD protection to be brought up to that standard whenever a switchboard is replaced — which a 3-phase upgrade always does. Switchboard installation is Clause 2.10: 1.0m clear of accessible faces of a closed board, 600mm unobstructed with doors open, IP2X indoors and IP33 for unprotected outdoor equipment. The main switch must be rated for the maximum demand determined under Clause 2.2.2 and Appendix C, voltage drop must stay within 5% under Clause 3.6, and individual RCBOs aren't mandated but are the sane choice on a three-phase board. A compliance certificate must be issued for the work."
  - question: "How long does a 3-phase power upgrade take?"
    answer: "The on-site work is 1–2 days. The clock that matters is administrative: the DNSP application has to be lodged and approved before anything is ordered, and that is where jobs blow out to weeks — a supply upgrade is separately assessed, so the 5–10 business-day solar connection targets do not apply. Then the meter, then certification. Only the contractor can lodge the application: it carries maximum demand calculations, a site plan and compliance declarations, and it has to come from the party signing the certificate."
  - question: "Do I need council approval for a 3-phase upgrade?"
    answer: "No — it's electrical work, not building work. The approvals that do apply are the DNSP connection application and the state electrical certificate. Council only enters the picture if the board or meter position moves in a way that triggers planning or heritage consent, which is a property-specific question, not a 3-phase one."
---

A 3-phase power upgrade costs $3,000–$10,000 in Australia, and getting it wrong — skipping the DNSP application, undersizing the switchboard, or failing to issue a CCEW — can leave your customer with a non-compliant installation and **you** facing a defect notice from the state regulator.

---

## What Is a 3-Phase Power Upgrade?

A 3-phase power upgrade converts a property's electrical supply from single-phase (one active conductor at 230V to neutral) to 3-phase (three active conductors at 230V each, 120° apart, 400V nominal between phases — commonly quoted on site as 415V). Under **AS/NZS 3000:2018**, this requires a new main switchboard rated for the maximum demand calculation, RCD protection on every final sub-circuit (Clause 2.6), and a compliance certificate — CCEW in NSW, COES in Victoria, certificate of testing and compliance in Queensland — issued by a licensed electrical contractor. The upgrade enables 30kW of solar inverter capacity, 22kW three-phase EV charging, and simultaneous operation of high-draw equipment without voltage drop.

---

## What Triggers a 3-Phase Upgrade?

Most Australian homes run on single-phase 80A or 100A supplies. That's fine for standard loads — but the following scenarios make a 3-phase upgrade essential, not optional:

**Solar above 10kW inverter capacity.** Ausgrid and Energex both approve up to 10kW of inverter capacity per phase through their streamlined processes, so a single-phase home can legitimately carry a 10kW inverter without touching the supply. Three-phase takes that to 30kW (10kW per phase) on the same basic approval — above 30kW in NSW you're into a technical assessment, and above 200kVA you're a negotiated connection. Inverter size and export limit are two different numbers: Energex approves a 10kW single-phase inverter to *export* 5kW, and Ausgrid's flexible-export connections default to 10kW per phase but fall back to a fixed 3kW per system if the customer opts out.

If a customer wants a 13kW system on a single-phase supply, that's when the arithmetic starts pointing at the upgrade. And note the oversizing separate from all of this: the DC array can exceed the inverter rating (the 133% DC/AC ratio is the common ceiling), but the DNSP limit is on inverter nameplate, not panel wattage.

**EV charger installation.** A single-phase 7.4kW EV charger pulls 32A continuously. Add a ducted air conditioner (15A), an oven (20A), and a pool pump (10A), and you've blown past the 80A maximum demand on a single-phase supply. A 3-phase supply lets you put the EV charger on one phase and everything else on the other two.

**Workshop or home business equipment.** Welders, 3-phase compressors, commercial kitchen equipment, and large ducted air conditioning all require 3-phase. A 15A single-phase welder is a toy compared to a 32A 3-phase unit.

**Future-proofing for home batteries.** If your customer is considering a Tesla Powerwall 3 or a 3-phase battery system, the 3-phase upgrade is the foundation. Retrofit later costs more.

---

## 3-Phase Upgrade Costs — Real 2026 Numbers

These are Australian dollar ranges from actual electrical contractor quotes in 2026. Every job is different, but here's what your customer is paying for:

| Component | Cost Range (AUD) | What Drives the Price |
|---|---|---|
| Switchboard replacement/upgrade | $1,500–$4,000 | Board size, RCD count, IP rating, fault current rating |
| DNSP service connection fee | $500–$1,500 | Network provider, overhead vs underground, meter position |
| Cable run (switchboard to point of attachment) | $500–$2,000 | Distance, accessibility, trenching required |
| Smart meter (3-phase capable) | $300–$700 | Meter type, retailer coordination |
| Level 2 ASP labour | $800–$1,500 | Connection complexity, travel, after-hours |
| **Total (typical residential)** | **$3,000–$10,000** | |

**What makes a job hit the $10,000 end:**
- Switchboard in an asbestos-backed panel from 1965
- 30-metre underground cable run through a concrete driveway
- Meter position relocation required by the DNSP
- Heritage overlay requiring a complying development certificate

**What keeps it at $3,000:**
- Modern switchboard with space for 3-phase main switch
- Overhead supply with short point-of-attachment run
- Meter position compliant with DNSP requirements
- No trenching, no structural work

---

## The Upgrade Process — Step by Step

### 1. Load Assessment and Maximum Demand Calculation

Before touching anything, calculate the maximum demand per **AS/NZS 3000:2018 Appendix C**. This determines:
- Main switch rating (typically 63A or 80A 3-phase for residential)
- Sub-circuit distribution across phases
- Whether the existing consumer mains cable is adequate

A single-phase 16mm² consumer mains might carry 80A single-phase fine — but with 3-phase loads, you may need 16mm² or 25mm² 4-core + earth.

### 2. DNSP Application

Every DNSP requires a **connection application** before the upgrade. This is the step homeowners skip that causes the most problems. You submit:
- Electrical contractor licence number
- Maximum demand calculation
- Site plan showing meter position and point of attachment
- Proposed switchboard location and IP rating
- Solar/EV load details if applicable

DNSPs vary wildly:
- **Ausgrid (NSW):** connection application lodged through the Connections portal; Level 2 ASP required for the physical connection
- **Endeavour Energy (NSW):** ASP Level 2 required; minimum 10 business days for a simple connection
- **Energex (QLD):** Electrical Work Request (EWR) lodged through the Electrical Partners Portal — the "Form A / Form B" pair is legacy and no longer how connections are lodged; the certificate of testing and compliance is separate (ES Regulation 2013 s227)
- **SA Power Networks:** online portal application; service connection fee scales with demand
- **Western Power (WA):** Residential Connection Application; Western Power does the meter install
- **TasNetworks:** connection application via the Connections Portal, plus the Certificate of Electrical Compliance (CEC) submitted to TechSafe Australia

### 3. Switchboard Upgrade to AS/NZS 3000:2018

Replace or upgrade the existing switchboard to comply with **Clause 2.10** (switchboards) and **Clause 2.6** (additional protection by RCD):

**Main switch:** rated for the calculated maximum demand — Clause 2.2.2 requires that maximum demand be determined for consumer mains and submains, and Appendix C (Tables C1–C3) is the deemed-to-comply method. A 3-phase 63A main switch is typical for residential; commercial 3-phase may need 100A or 160A. Main switches must be manually operated, not controlled by electronic devices.

**RCD protection (Clause 2.6):** In domestic and residential installations, 30mA RCDs are required on all final sub-circuits (Clause 2.6.3.2.2) with no exceptions, installed at the switchboard from which the sub-circuit originates. For non-domestic work the obligation attaches to socket-outlet and lighting circuits ≤32A plus fixed-wired equipment up to 32A that presents an increased risk of shock. Critically for this job: **Clause 2.6.3.2.5** requires RCD protection to be brought up to those standards whenever a switchboard is replaced or a final sub-circuit is altered — you cannot re-use an unprotected board on a 3-phase changeover. Individual RCBOs per circuit aren't mandated, but they are industry best practice because a single shared RCD takes the whole board out on one fault.

**IP rating (Clause 2.10 / Section 1):** IP2X minimum indoors against contact with live parts. Outdoors is stricter than most tradies assume: equipment needs **at least IP33**, except meter panels which are IP23-rated, and there's a 30° triangular zone under an eave or veranda where IP2X equipment is still acceptable.

**Clearances (Clause 2.10):** 1.0m clear from accessible faces of a closed switchboard, and 600mm unobstructed around the board with doors open or equipment racked out. Switch rooms need more again — 2.2m door height, 0.9m door width, and two egress paths above 800A or past 3m in length.

**Fault current rating:** The switchboard must be rated for the prospective short-circuit current at the point of installation. For a residential 3-phase supply, typically 6kA minimum. DNSPs can advise the fault level at the connection point.

### 4. Level 2 ASP Connection

The physical connection between the DNSP network and the property must be done by a **Level 2 Authorised Service Provider (ASP)** in NSW and QLD, or the equivalent in other states. This is not optional — standard electrical contractors cannot touch the network side.

The Level 2 ASP will:
- Run or upgrade the consumer mains from the point of attachment to the switchboard
- Connect the new 3-phase service from the street
- Install the 3-phase meter isolation link
- Coordinate with the metering provider

### 5. Metering

Your customer's electricity retailer installs the 3-phase smart meter. This is coordinated between the Level 2 ASP, the retailer, and the metering coordinator. Timeline: 1–4 weeks after the ASP connection.

**Critical point:** The old single-phase meter cannot measure 3-phase consumption. If the customer uses 3-phase power before the new meter is installed, they're unmetered — and they'll get an estimated bill based on their highest historical consumption. Coordinate the meter install to happen within days of the ASP connection.

### 6. Testing, Verification, and Compliance Certificate

After installation, mandatory testing per **AS/NZS 3000:2018 Section 8** (8.2 inspection, 8.3 test methods and criteria):
- Earth fault loop impedance at every point
- RCD operation: ≤300ms at rated residual current (IΔn), ≤40ms at 5×IΔn
- Insulation resistance (≥1MΩ on all circuits)
- Polarity and phase rotation
- Prospective short-circuit current verification at the main switch

Then, issue the state-specific compliance certificate:
- **NSW:** CCEW (Certificate of Compliance Electrical Work) — required under the Gas and Electricity (Consumer Safety) Regulation 2018 (s37A) and lodged to Building Commission NSW via the eCert portal within 7 days of the safety and compliance test
- **Victoria:** COES (Certificate of Electrical Safety) — mandatory under the Electricity Safety Act 1998, administered by Energy Safe Victoria. A switchboard change is **prescribed** electrical work, so an independent Licensed Electrical Inspector must inspect it. ESV's sequence: the responsible person completes and signs the COES within 4 business days of finishing the work, gives the electronic notification to ESV within 2 business days of completing the certificate, and the inspection must happen within 8 business days of the work being completed. The inspector lodges their Certificate of Inspection and returns the COES to the responsible person within 4 business days, and the responsible person then distributes all copies within 4 business days of receiving it. Keep your copy for 3 years. The 30-day figure that circulates in the trade is the non-prescribed deadline.
- **Queensland:** Certificate of testing and compliance (ES Regulation 2013 s227) — issued to the customer as soon as practicable after the installation is connected, copy retained five years; the connection itself is lodged as an EWR
- **South Australia:** electronic Certificate of Compliance (eCoC) — submitted to the Office of the Technical Regulator within 30 days of completing the work, and required before SA Power Networks will connect
- **Western Australia:** Notice of Completion — administered by Building and Energy
- **Tasmania:** Certificate of Electrical Compliance (CEC) — submitted to TechSafe Australia within 3 days of the work being energised or capable of being energised, with the CEC number quoted on the TasNetworks EWR

---

## AS/NZS 3000:2018 Requirements — The Compliance Checklist

When a state electrical inspector audits a 3-phase upgrade, these are the clauses they check. Every item is a potential defect notice:

**Clause 2.10 — Switchboards:**
- Maximum demand calculation documented and main switch rated accordingly (Clause 2.2.2, Appendix C)
- 1.0m clear of accessible faces of a closed board; 600mm unobstructed with doors open
- IP rating appropriate for the location — IP2X indoors, IP33 unprotected outdoors, IP23 for meter panels
- Switchboard rated for the prospective fault current at that point

**Clause 2.6 — RCD Protection:**
- 30mA RCD on all final sub-circuits in domestic/residential installations (2.6.3.2.2), and RCDs added whenever the board is replaced or a circuit altered (2.6.3.2.5)
- RCD installed at the board from which the sub-circuit originates
- RCD trip time verified and recorded — ≤300ms at IΔn, ≤40ms at 5×IΔn
- RCD test button functional and test date recorded

**Clause 5.3 — Earthing:**
- MEN connection verified at the main switchboard
- Earth electrode and main earthing conductor of adequate size and resistance for the fault-loop calculation to hold — the electrode must be one that, with the rest of the loop, lets the protective device disconnect within the required time. There is no fixed ohm figure written into the Wiring Rules; if you're quoting a resistance, quote the one your fault-loop calculation depends on
- Equipotential bonding to all metallic services (water, gas, communications)

**Clause 3.6 — Voltage Drop and Consumer Mains:**
- Cable size adequate for maximum demand + voltage drop, capped at 5% total from the point of supply to the furthest point of utilisation (mains, submains and final sub-circuit combined — it is a single 5% budget, not 5% per leg)
- Protection device at the origin of the consumer mains (Clause 2.5.1.2)
- Labelling of all submains and distribution boards

**Section 8 — Verification:**
- All mandatory test results recorded and signed (8.2 inspection, 8.3 tests)
- Compliance certificate issued on time — 7 days from the test in NSW; in VIC the prescribed-work COES clock (4 days to sign, 2 days to notify ESV, 8 days to inspection)
- Copy provided to the customer and filed with the regulator

A **single missing RCD on one final sub-circuit** will fail an inspection in any state. The defect notice process costs the contractor time and reputation — and in NSW, repeat non-compliance can trigger a licence review by Building Commission NSW under the Gas and Electricity (Consumer Safety) Act 2017.

---

## State-by-State DNSP Differences

### NSW — Ausgrid and Endeavour Energy

Ausgrid covers Sydney, Central Coast, and Hunter. Endeavour Energy covers Western Sydney, Illawarra, and the Blue Mountains. Essential Energy covers regional NSW.

- **Application:** lodged through Ausgrid's Connections portal; the connection work itself needs a Level 2 ASP
- **ASP level:** Level 2 ASP required for connection
- **Fee range:** $500–$1,200 for a simple residential upgrade
- **Timeline:** supply upgrades are separately assessed — do not quote the solar application timeframes (Ausgrid's solar target is 5 business days up to 10kW, 10 business days for 10–30kW) as if they apply to a new 3-phase service

### VIC — Powercor, AusNet Services, United Energy, CitiPower, Jemena

Five DNSPs cover different parts of Victoria. A switchboard change is prescribed electrical work, so a prescribed COES with an inspector's sign-off is required under Energy Safe Victoria's scheme.

- **Application:** Via the DNSP's online portal. New connections require a Registered Electrical Contractor (REC) number
- **Metering:** Smart meter coordinated through the retailer; Victorian smart meters are already 3-phase capable in many cases
- **Fee range:** $400–$1,000
- **Timeline:** 5–15 business days, plus the LEI inspection window (8 business days) and 2-business-day notification to ESV

### QLD — Energex and Ergon Energy

Energex covers South East Queensland. Ergon covers the rest.

- **Application:** Electrical Work Request (EWR) through the Electrical Partners Portal; the certificate of testing and compliance under s227 is a separate document
- **Solar:** DER must be approved before installation, and applications are lodged through the same portal — Energex and Ergon forms are not interchangeable
- **Fee range:** $600–$1,500
- **Timeline:** 10–20 business days; longer in regional Ergon areas

### SA — SA Power Networks

- **Application:** Online portal — residential connection application
- **Fee range:** $500–$1,000; scales with demand
- **Certification:** electronic Certificate of Compliance (eCoC) lodged with the Office of the Technical Regulator within 30 days; a valid eCoC must exist before SA Power Networks will make the final connection
- **Timeline:** 5–10 business days for metro, 10–20 for regional

### WA — Western Power

- **Application:** Residential Connection Application via online portal
- **Fee range:** $500–$1,200; Western Power publishes $586–$853 for an overhead single-to-three-phase conversion
- **Metering:** Western Power installs the meter directly; no separate metering coordinator
- **Timeline:** 10–20 business days

### TAS — TasNetworks

- **Application:** Connection application through the Connections Portal; above 100A per phase (or where network changes are needed) it becomes a negotiated connection with design costs payable up front
- **Certification:** Certificate of Electrical Compliance (CEC) to TechSafe Australia within 3 days of energising, CEC number quoted on the EWR
- **Fee range:** $500–$1,000
- **Timeline:** 10–15 business days

---

## Where the Upgrade Goes Wrong — Common Failure Modes

### 1. No DNSP Application Before Work Starts

The homeowner books you for Tuesday. You show up, rip out the old switchboard, install the new 3-phase board, and call the DNSP for connection — and they tell you there's a 15-business-day application queue. The customer has no power for three weeks. This is the #1 complaint on electrical contractor forums. **Always submit the DNSP application before ordering the switchboard.**

### 2. Single-Phase Cables in a 3-Phase Board

The existing 16mm² 2-core + earth consumer mains carries single-phase fine. But 3-phase needs 4-core + earth, and 16mm² may not be enough. A 63A 3-phase supply with 25m cable run will drop voltage below compliance if the cable is undersized. Run the voltage drop calculation before quoting.

### 3. No RCD on the Metered Load Circuit

Some installers put RCDs on every sub-circuit but leave the main switch side unprotected. AS/NZS 3000:2018 Clause 2.6.3.2.2 requires 30mA RCD protection on **all final sub-circuits** in domestic and residential installations — that includes any circuit downstream of the main switch. The meter isolator doesn't count as a sub-circuit, but anything after it does. And because a 3-phase upgrade always replaces the board, Clause 2.6.3.2.5 applies: RCD protection has to be brought up to the current requirement, not matched to whatever the old single-phase board had.

### 4. CCEW/COES Not Filed Within the Deadline

NSW requires the CCEW to be lodged within 7 days of the safety and compliance test (Gas and Electricity (Consumer Safety) Regulation 2018, s37A) via the Building Commission NSW eCert portal. Victoria is where this goes wrong most often: a 3-phase upgrade replaces the switchboard, which is **prescribed** work, so it needs an inspector and a prescribed COES — signed within 4 business days of finishing the work, notified to ESV within 2 business days of the certificate being completed, inspected within 8 business days, then copies distributed within 4 business days of the inspector returning it. Contractors who budget on the 30-day non-prescribed figure miss every one of those windows. Missing a deadline triggers an automatic audit flag in the regulator's system, and the audit looks at the entire job — not just the late certificate.

### 5. No Future-Proofing

While the switchboard is open and the DNSP is connecting a new 3-phase supply, this is the cheapest moment to add:
- A dedicated EV charger circuit with 6mm² cable and a 40A RCBO
- A solar-ready meter panel with space for a generation meter
- A submain to the garage or shed for future equipment

Retrofitting any of these after the board is closed and certified costs $500–$2,000. Adding them during the initial upgrade adds $50–$300 in materials.

---

## Cross-Sell Opportunities — What to Quote Alongside the 3-Phase Upgrade

A 3-phase upgrade opens the door to three high-value add-ons that make the job more profitable and the property more functional:

### Solar-Ready Prep
With 3-phase in place, your customer can install up to 30kW of inverter capacity (10kW per phase) on a standard basic connection in NSW and QLD. Quote the solar meter panel, a dedicated solar circuit in the switchboard, and lodge the DER application through the DNSP portal alongside the service connection — in Queensland the DER approval has to exist before the panels go on. The incremental cost is low — the big cost is already sunk in the upgrade.

### EV Charger Circuit
Pull the cable now while the switchboard is open. A 32A single-phase (7.4kW) or 32A 3-phase (22kW) circuit to the garage adds $200–$500 in materials during the upgrade vs $1,500–$3,000 if trenched separately later. Even if the customer doesn't have an EV yet, the circuit is there.

### ServiceM8 Job Management
A 3-phase upgrade is a multi-day, multi-trade job — you, a Level 2 ASP, the meter provider, and potentially a builder for trenching. Running it through [ServiceM8 for Electricians](/blog/servicem8-for-electricians/) keeps the DNSP application deadline, compliance certificate expiry, and subcontractor coordination in one place. [Try ServiceM8 free →](https://www.servicem8.com/?ref=tradieautomate&utm_source=tradieautomate&utm_medium=blog&utm_campaign=affiliate)

---

## FAQ

### How much does a 3-phase power upgrade cost in Australia?

A single-phase to 3-phase upgrade in Australia typically runs **$3,000–$10,000**: switchboard replacement $1,500–$4,000, the DNSP connection fee $500–$1,500, cable run $500–$2,000, a three-phase smart meter $300–$700, and Level 2 ASP labour $800–$1,500. The $10,000 end is asbestos-backed boards, long underground runs through concrete, and meter relocations. Western Power publishes $586–$853 for an overhead single-to-three-phase conversion; that's the network side only, not the board.

### Do I need a 3-phase upgrade for solar or an EV charger?

Usually not for solar alone. Ausgrid and Energex both approve up to 10kW of inverter capacity per phase, so a single-phase home can carry a 10kW inverter without a supply upgrade — 30kW is the three-phase ceiling on the same streamlined approval. Above 10kW per phase in NSW you move to a technical assessment. A 3-phase upgrade is justified when the customer needs more than 10kW of inverter, wants 22kW three-phase EV charging, or already has single-phase loads pressed against a 63A–80A supply. Keep export limits separate from inverter limits: Energex approves a 10kW single-phase inverter to export 5kW.

### What are the AS/NZS 3000 requirements for a 3-phase switchboard upgrade?

Clause 2.6 requires 30mA RCD protection on all final sub-circuits in domestic installations (2.6.3.2.2), and 2.6.3.2.5 requires RCD protection to be brought up to that standard whenever a switchboard is replaced — which a 3-phase upgrade always does. Switchboard installation is Clause 2.10: 1.0m clear of accessible faces of a closed board, 600mm unobstructed with doors open, IP2X indoors and IP33 for unprotected outdoor equipment. The main switch must be rated for the maximum demand determined under Clause 2.2.2 and Appendix C, voltage drop must stay within 5% under Clause 3.6, and individual RCBOs aren't mandated but are the sane choice on a three-phase board. A compliance certificate must be issued for the work.

### How long does a 3-phase power upgrade take?

The on-site work is 1–2 days. The clock that matters is administrative: the DNSP application has to be lodged and approved before anything is ordered, and that is where jobs blow out to weeks — a supply upgrade is separately assessed, so the 5–10 business-day solar connection targets do not apply. Then the meter, then certification. Only the contractor can lodge the application: it carries maximum demand calculations, a site plan and compliance declarations, and it has to come from the party signing the certificate.

### Do I need council approval for a 3-phase upgrade?

No — it's electrical work, not building work. The approvals that do apply are the DNSP connection application and the state electrical certificate. Council only enters the picture if the board or meter position moves in a way that triggers planning or heritage consent, which is a property-specific question, not a 3-phase one.

---

## Related Articles

- [CCEW NSW Electrical Compliance Guide 2026](/blog/ccew-nsw-electrical-compliance-guide-2026/) — Certificate of compliance requirements for the upgrade
- [Electrical Contractor Insurance Guide Australia 2026](/blog/electrical-contractor-insurance-australia-2026/) — Insurance implications of switchboard work
- [RCD Safety Switch Requirements AS/NZS 3000](/blog/rcd-safety-switch-requirements-as-nzs-3000-electricians-2026/) — RCD compliance after the upgrade
- [ServiceM8 for Electricians](/blog/servicem8-for-electricians/) — Job management for multi-day upgrade jobs