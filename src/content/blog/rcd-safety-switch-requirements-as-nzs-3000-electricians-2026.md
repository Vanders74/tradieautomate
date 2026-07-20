---
title: "RCD Safety Switch Requirements Under AS/NZS 3000 — Electricians' 2026 Guide"
description: "AS/NZS 3000:2018 Amd 2 expanded mandatory RCD coverage significantly. Which circuits need protection, which RCD type (AC, A, F, B) applies to solar and EV chargers, and what auditors check on switchboard upgrades."
pubDate: 'Jul 20 2026'
updatedDate: 'Jul 20 2026'
category: "Compliance"
heroImage: '/hero-compliance-safety-2026.jpg'
tags: ['RCD', 'safety switch', 'AS/NZS 3000', 'switchboard', 'electrician', 'compliance', 'solar', 'EV charger']
faq:
  - question: "Which circuits require RCD protection under AS/NZS 3000:2018?"
    answer: "Under AS/NZS 3000:2018 Clause 2.6.1 (including Amendment 2), RCD protection at 30mA or less is mandatory for all socket outlet circuits, lighting circuits in residential dwellings, and circuits supplying equipment in outdoor areas, bathrooms, laundries, and kitchens. In new residential installations and full switchboard replacements, all final sub-circuits require RCD protection. Commercial and industrial installations have additional requirements based on occupancy classification."
  - question: "What RCD type do I need for a solar inverter installation?"
    answer: "Solar grid-connect inverters produce DC fault currents that can blind standard Type AC RCDs. AS/NZS 3000:2018 and inverter manufacturer specifications require a minimum Type A RCD for single-phase solar inverters. Three-phase inverters and those with transformerless topologies typically require a Type B RCD. Always check the specific inverter manufacturer's installation manual — this is a common CER audit failure point."
  - question: "What RCD type is required for EV charger installations in Australia?"
    answer: "EV chargers (EVSE) produce DC leakage currents during normal operation. Most EV charger manufacturers specify a Type B RCD as the minimum requirement for their equipment under AS/NZS 3000. Type F RCDs are suitable for variable frequency drive loads but may not cover all DC leakage characteristics. Type B is the safest specification and is increasingly required by DNSP technical standards. Check both the equipment manual and your DNSP's requirements before specifying."
  - question: "Does a switchboard upgrade trigger full RCD retrofitting under AS/NZS 3000?"
    answer: "Yes. A switchboard replacement (not just a circuit addition) triggers the requirement to upgrade all final sub-circuits to meet current AS/NZS 3000 requirements, including RCD protection. Adding new circuits to an existing board is treated differently — the new circuits must comply, but existing circuits on that board are not automatically required to be upgraded unless the overall installation is classified as substantially altered. The definition of 'substantially altered' requires judgment and varies by state regulator interpretation."
  - question: "What is the difference between Type AC, Type A, Type F, and Type B RCDs?"
    answer: "Type AC RCDs detect only sinusoidal AC fault currents. Type A detects sinusoidal AC and pulsating DC fault currents — required for single-phase solar inverters and most residential applications involving electronics. Type F detects sinusoidal AC, pulsating DC, and high-frequency leakage from variable-speed drives. Type B detects all of the above plus smooth DC fault currents — required for most EV chargers and three-phase solar inverters with DC injection risk."

---

Under **AS/NZS 3000:2018 Clause 2.6.1**, every circuit supplying socket outlets in a residential dwelling requires RCD protection at 30mA or less. Amendment 2 to the standard, adopted progressively across Australian states from 2023, has expanded this coverage significantly — and the wrong RCD type on a solar inverter or EV charger is now a documented CER audit failure point.

This guide covers what changed, which circuits need protection, which RCD type applies to each application, and what state regulators and auditors check on-site.

---

## What Changed: AS/NZS 3000:2018 and Amendment 2

**AS/NZS 3000** is Australia and New Zealand's Wiring Rules standard — the foundational document governing electrical installation compliance. The 2018 edition replaced the 2007 edition, and **Amendment 2** (released in 2022, progressively mandated across states from 2023) made substantive changes to RCD requirements.

Key changes from Amendment 2:

1. **Extended mandatory RCD coverage** to lighting circuits in all residential dwellings (previously required only for socket outlets)
2. **Clarified the "new installation" trigger** — a full switchboard replacement now explicitly triggers whole-board RCD compliance
3. **Introduced RCD type requirements** for inverter-connected circuits — Type A as a minimum for solar, Type B for DC-capable loads including EV chargers
4. **Tightened testing documentation requirements** (AS/NZS 3017) for installed RCDs

The practical effect: jobs that were compliant under AS/NZS 3000:2007 may not comply with the current standard. Every switchboard upgrade and solar installation must be assessed against the 2018 edition with Amendment 2.

---

## Which Circuits Require RCD Protection

### Residential Dwellings

Under AS/NZS 3000:2018 with Amendment 2, the following circuits in a residential dwelling require RCD protection at ≤30mA:

| Circuit Type | RCD Required? | Notes |
|---|---|---|
| Socket outlet circuits (all) | Yes | All final sub-circuits supplying socket outlets |
| Lighting circuits | Yes (Amd 2) | All lighting in dwellings — this is the key change |
| Outdoor circuits | Yes | Any circuit with external socket outlets |
| Bathroom/laundry circuits | Yes | Includes shaver outlets |
| Kitchen circuits | Yes | Including fixed appliance circuits |
| Garage/carport socket outlets | Yes | Treated as outdoor circuits |
| Fixed air conditioning (residential) | Generally yes | Check installation conditions |

**What does not require RCD protection in residential:**
- Circuits protected by other safety measures meeting equivalent electrical safety outcomes (rare and requires specific engineering assessment)
- Exempt circuits as specified in the standard (e.g. circuits where RCD operation would itself create a safety hazard — emergency lighting in some contexts)

### Commercial and Industrial

Commercial and industrial RCD requirements are occupancy-specific. Key triggers:

- **Class 2–4 buildings** (flats, boarding houses, hotels): treated similarly to residential for inhabited areas
- **Construction sites (AS/NZS 3012):** all portable tools and temporary supplies require RCD protection — this is separate from AS/NZS 3000
- **Healthcare facilities:** specific RCD and medical isolation transformer requirements under AS/NZS 3003
- **Swimming pools and spas:** AS/NZS 3000 Section 7.3 — equipotential bonding and RCD requirements vary by pool type

---

## RCD Types: Which Application Requires What

This is where most compliance failures occur. Specifying the wrong RCD type creates an audit fail regardless of whether an RCD is installed at all.

**Type AC**
Detects sinusoidal AC fault currents only. Suitable for simple resistive and inductive loads with no electronics — think basic socket outlet circuits with no inverter or variable-speed drive involvement.

*Do not use Type AC on circuits serving solar inverters, EV chargers, or variable-speed drives.*

**Type A**
Detects sinusoidal AC and pulsating DC fault currents. Required as the minimum for:
- Single-phase solar inverters (grid-connect)
- Most modern appliance circuits with switch-mode power supplies
- General residential circuits where electronics are connected

Type A is now the practical baseline for residential work. Installing Type AC on a circuit that will serve solar or a modern appliance creates non-compliance immediately upon connection.

**Type F**
Detects sinusoidal AC, pulsating DC, and high-frequency leakage currents from variable-frequency drives. Required for:
- Air handling units with VFD-controlled fans
- Industrial machinery with variable-speed motor drives
- Some HVAC systems

Type F is uncommon in residential but increasingly relevant in commercial electrical work.

**Type B**
Detects all fault current types including smooth DC up to several kHz. Required for:
- Most EV chargers (EVSE) — both Mode 2 and Mode 3
- Three-phase solar inverters with DC injection potential
- Battery storage systems with DC-connected inverters
- Any load with a rectifier bridge producing smooth DC output

| Application | Minimum RCD Type |
|---|---|
| Standard socket outlets (residential) | Type A |
| Lighting circuits | Type A |
| Single-phase solar inverter | Type A (check inverter specs — may require Type B) |
| Three-phase solar inverter | Type B |
| Battery storage (DC-coupled) | Type B |
| EV charger (Mode 3, single-phase) | Type B |
| EV charger (Mode 3, three-phase) | Type B |
| Variable frequency drives | Type F or Type B |

**Practical rule:** When in doubt, specify Type B. The cost premium is modest compared to a failed audit or a warranty void from the equipment manufacturer.

---

## Switchboard Upgrades: When Does Full Retrofitting Apply?

This is the grey area that generates the most compliance questions.

**Full switchboard replacement:** Installing a new switchboard — removing the old board and fitting a new one — triggers full compliance with AS/NZS 3000:2018 on all circuits connected to that board. Every final sub-circuit must receive RCD protection compliant with the current standard.

**Adding new circuits to an existing board:** The new circuit must comply with AS/NZS 3000:2018. Existing circuits on the board are not automatically required to be upgraded unless the installation is "substantially altered."

**"Substantially altered" definition:** This is not precisely defined in AS/NZS 3000 and is subject to state regulator interpretation. As a rule of practice:

- Adding 1–2 new circuits: typically not substantially altered
- Replacing the main switch, upgrading the incomer, or reconfiguring the board layout: likely substantially altered, triggering full compliance assessment
- Adding solar or EV charger circuits that increase total load by more than 30% of the existing board's rated capacity: increasingly being treated as substantially altered by Energy Safe Victoria and SafeWork NSW

**Energy Safe Victoria's specific stance:** ESV's Technical Bulletin TB-080 notes that solar inverter installations that involve the existing switchboard must be assessed against current wiring rule requirements for the circuits affected. This has been used to require RCD retrofitting on solar installs where the existing board had no RCD protection.

When uncertain, apply the current standard to the entire board. The cost of an RCD-per-circuit retrofit is orders of magnitude less than a failed inspection and remediation.

---

## State Variations in Enforcement

**Victoria (Energy Safe Victoria)**
ESV is the most active enforcer of AS/NZS 3000 technical requirements in Australia. Amendment 2 requirements have been incorporated into ESV's compliance framework. CES audit teams check RCD type compliance specifically on solar and battery installations.

**NSW (SafeWork NSW)**
SafeWork NSW enforces via the CCEW (Certificate of Compliance for Electrical Work) submission process. CCEWs that certify work not meeting AS/NZS 3000 requirements expose the certifying electrician to prosecution under the Electricity (Consumer Safety) Act 2004. NSW audits of unlicensed or defective electrical work have increased since 2024.

**Queensland (Electrical Safety Office)**
ESO Queensland requires all electrical work to comply with the current edition of AS/NZS 3000. The ESO's audit program has specifically focused on solar installations with incorrect RCD types. Queensland's Form 4 (Compliance Certificate) requires the certifying person to confirm compliance with the current standard.

---

## Testing Requirements: AS/NZS 3017

Installed RCDs must be tested and results documented under **AS/NZS 3017 — Electrical Installations: Verification Guidelines**.

Required tests per RCD:

1. **Trip time test:** Apply 1× rated residual current (e.g. 30mA for a 30mA RCD). Trip time must be ≤300ms for Type AC/A, with faster requirements for some Type F and B devices.
2. **Ramp test:** Apply increasing current until trip — confirms the trip threshold matches the rating.
3. **Test button verification:** Manual test button must operate correctly.

**Documentation required:**
- Measured trip time for each RCD
- Test instrument model and calibration date
- Circuit identification
- Technician name and licence number

CER auditors and state regulator inspectors increasingly check for RCD test records as part of site compliance verification for solar and battery installations. Undocumented RCDs — even correctly installed ones — create a compliance gap.

---

## How ServiceM8 Supports Compliance Documentation

Maintaining RCD test records, linking them to job files, and retrieving them for audits is where paper-based systems fall apart. ServiceM8 lets you:

- Attach RCD test results directly to the job record
- Generate structured electrical compliance job cards with test fields built in
- Set automatic reminders for periodic RCD testing on recurring maintenance contracts
- Build CCEW and Form 4 compliance into your standard job close-out workflow

[Start your free ServiceM8 trial →](https://www.servicem8.com/?ref=tradieautomate)

---

## FAQ

### Which circuits require RCD protection under AS/NZS 3000:2018?

All socket outlet circuits, all lighting circuits in residential dwellings, and circuits serving outdoor areas, bathrooms, laundries, and kitchens. Amendment 2 added lighting circuits as a mandatory requirement — the most significant change for residential electricians.

### What RCD type do I need for a solar inverter installation?

Minimum Type A for single-phase inverters. Type B for three-phase inverters and any inverter with DC injection risk. Always check the inverter manufacturer's installation manual — manufacturers specifying Type B in their manual make Type A a non-compliance at the CEC level even if AS/NZS 3000 would accept Type A.

### What RCD type is required for an EV charger?

Type B is required for most EV chargers (Mode 3 AC charging equipment). This covers DC leakage currents that Type AC, A, and F devices cannot detect. Confirm with the charger manufacturer's installation documentation and your DNSP's technical standards.

### Does replacing a switchboard trigger full RCD compliance on all circuits?

Yes. A full switchboard replacement triggers compliance with AS/NZS 3000:2018 (Amendment 2) on all circuits. Adding circuits to an existing board requires only the new circuits to comply, unless the installation is substantially altered.

### What does "substantially altered" mean under AS/NZS 3000?

The standard does not precisely define this term. In practice, it encompasses switchboard layout changes, incomer upgrades, and load additions that materially change the installation's character. When uncertain, apply the current standard to the whole board.

---

## Related Reading

- *[Electrical Switchboard Upgrade Cost Australia 2026](/blog/electrical-switchboard-upgrade-cost-australia-2026)*
- *[Solar Compliance Checklist for Australian Installers (2026)](/blog/solar-compliance-checklist-2026)*
- *[Staying Compliant in 2026: The Complete Safety and Compliance Guide](/blog/staying-compliant-2026-solar-electrical-safety)*
- *[CER Audit Prep: How to Pass Your Clean Energy Regulator Audit](/blog/cer-audit-prep-solar-installers)*
- *[Commercial EV Charging Installation: The Electrician's Business Guide for 2026](/blog/commercial-ev-charging-installation-guide-electricians)*
- *[EV Charger Installation Business Case for Electricians 2026](/blog/ev-charger-installation-business-case-electricians-2026)*

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Which circuits require RCD protection under AS/NZS 3000:2018?","acceptedAnswer":{"@type":"Answer","text":"All socket outlet circuits, all lighting circuits in residential dwellings (Amendment 2 change), and circuits serving outdoor areas, bathrooms, laundries, and kitchens."}},{"@type":"Question","name":"What RCD type do I need for a solar inverter installation?","acceptedAnswer":{"@type":"Answer","text":"Minimum Type A for single-phase inverters. Type B for three-phase inverters and any inverter with DC injection risk. Always check the inverter manufacturer's installation manual."}},{"@type":"Question","name":"What RCD type is required for an EV charger?","acceptedAnswer":{"@type":"Answer","text":"Type B is required for most EV chargers (Mode 3 AC charging equipment). This covers DC leakage currents that Type AC, A, and F devices cannot detect."}},{"@type":"Question","name":"Does replacing a switchboard trigger full RCD compliance on all circuits?","acceptedAnswer":{"@type":"Answer","text":"Yes. A full switchboard replacement triggers compliance with AS/NZS 3000:2018 on all circuits connected to that board."}},{"@type":"Question","name":"What is the difference between Type AC, A, F, and B RCDs?","acceptedAnswer":{"@type":"Answer","text":"Type AC: AC fault currents only. Type A: AC and pulsating DC — minimum for solar inverters. Type F: AC, pulsating DC, and high-frequency VFD leakage. Type B: all types including smooth DC — required for EV chargers and three-phase solar."}}]}
</script>
