---
title: 'RCD Safety Switch Requirements: AS/NZS 3000 Types A/B/F'
description: "What AS/NZS 3000:2018 actually requires: 30mA RCDs on every residential final subcircuit, the Type AC ban since 30 April 2023, and which RCD type for solar and EV."
pubDate: 'Jul 20 2026'
updatedDate: 'Oct 18 2026'
category: "Compliance"
heroImage: '/hero-compliance-safety-2026.jpg'
tags: ['RCD', 'safety switch', 'AS/NZS 3000', 'switchboard', 'electrician', 'compliance', 'solar', 'EV charger']
faq:
  - question: "Which circuits require RCD protection under AS/NZS 3000:2018?"
    answer: "Every final subcircuit in a domestic or residential installation — socket outlets, lighting and fixed equipment such as ovens, hot water and air conditioning — under Clause 2.6.3.2.2. This has been the rule since the 2018 edition replaced the 2007 edition, which only covered socket outlet circuits. Amendment 2 added the Type AC ban, not the lighting coverage."
  - question: "What RCD type do I need for a solar inverter installation?"
    answer: "Type A as the general choice for single-phase inverters, unless the inverter manual specifies Type B — in which case the manufacturer's requirement governs and Type A is a non-compliance. Always check the installation manual before specifying."
  - question: "What RCD type is required for an EV charger?"
    answer: "Either a Type B RCD, or a Type A RCD with a 6mA RDC-DD (built into most Mode 3 chargers to IEC 62955). Type AC is prohibited. Confirm with both the charger's installation documentation and your DNSP's technical standards."
  - question: "Does replacing a switchboard trigger full RCD compliance on all circuits?"
    answer: "Yes. A full switchboard replacement triggers RCD protection under Clause 2.6.3.2.5 for all final subcircuits supplied by that board. Adding circuits to an existing board requires the new or altered circuits to comply; untouched circuits are not automatically upgraded."
  - question: "What does \"substantially altered\" mean under AS/NZS 3000?"
    answer: "The standard does not use that phrase — it talks about alterations to an installation and replacement of switchboards (Clauses 2.6.3.2.5 and 1.4.8). What matters is whether a circuit has been altered or had its source of supply changed. When uncertain, apply the current standard to the whole board. > **This article is featured in Chapter 2 of The Sparky's Playbook.** > The free 12-chapter guide for Australian electricians — licensing, EV charging, commercial solar, cash flow, tech stack, and building a business worth selling. > [Download the full book free →](/playbook)"
---

Under **AS/NZS 3000:2018 Clause 2.6.3.2.2**, every final subcircuit in a domestic or residential installation — socket outlets, lighting and fixed equipment alike — requires RCD protection at 30mA or less, installed at the switchboard where the circuit originates. Amendment 2 later added a separate rule in **Clause 2.6.2.2.2** that bans Type AC RCDs outright, and the wrong RCD type on a solar inverter or EV charger is now a documented CER audit failure point.

This guide covers what changed, which circuits need protection, which RCD type applies to each application, and what state regulators and auditors check on-site.

---


<div class="tool-cta-box">
  <div class="tc-inner">
    <div class="tc-text">
      <strong class="tc-title">💸 What rebates can you claim this job?</strong>
      <p class="tc-body">Free Rebate Finder — current state and federal incentives for switchboard upgrades, solar, batteries and heat pumps, checked weekly against regulator sources.</p>
    </div>
    <a href="/tools/rebate-finder/" class="tc-link">Find Rebates →</a>
  </div>
</div>

## What Changed: AS/NZS 3000:2018 and Amendment 2

**AS/NZS 3000** is Australia and New Zealand's Wiring Rules standard — the foundational document governing electrical installation compliance. The 2018 edition replaced the 2007 edition, and **Amendment 2** (published 30 April 2021) added the RCD type rules that now trip up solar and EV work.

Key changes from the 2018 edition and its amendments:

1. **Extended mandatory RCD coverage** — the 2018 edition already required 30mA protection on *all* final subcircuits in domestic and residential installations, not just socket outlet circuits as the 2007 edition did
2. **Banned Type AC RCDs** — Clause 2.6.2.2.2, inserted by Amendment 2, allowed a 24-month transition ending 30 April 2023, after which Type AC RCDs must not be installed in Australia
3. **Recommended Type A as the general type** for installations, given the growth in electronics, renewables and DC waveforms on the AC supply
4. **Clarified the alteration trigger** — Clause 2.6.3.2.5 requires RCD protection on circuits affected by alterations or a switchboard replacement

The practical effect: jobs that were compliant under AS/NZS 3000:2007 may not comply with the current standard, and a Type AC device on the shelf is no longer installable. Every switchboard upgrade and solar installation must be assessed against the 2018 edition with Amendment 2.

---

## Which Circuits Require RCD Protection

### Residential Dwellings

Under AS/NZS 3000:2018 Clause 2.6.3.2.2, every final subcircuit in a domestic or residential installation requires RCD protection at ≤30mA — there is no longer a socket-outlets-only rule:

| Circuit Type | RCD Required? | Notes |
|---|---|---|
| Socket outlet circuits (all) | Yes | All final sub-circuits supplying socket outlets |
| Lighting circuits | Yes | Required since the 2018 edition, not just Amd 2 |
| Outdoor circuits | Yes | Any circuit with external socket outlets |
| Bathroom/laundry circuits | Yes | Includes shaver outlets |
| Kitchen circuits | Yes | Including fixed appliance circuits |
| Garage/carport socket outlets | Yes | Treated as outdoor circuits |
| Fixed equipment (ovens, hot water, air conditioning) | Yes | Covered as final subcircuits in a dwelling |

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
Detects sinusoidal AC fault currents only. **Type AC RCDs must not be installed in Australia** — Clause 2.6.2.2.2 (Amendment 2) ended the transition period on 30 April 2023. Existing Type AC devices may stay in place if they test correctly, but they cannot be fitted to new work, new final subcircuits, or as a like-for-like replacement.

*On any circuit serving a solar inverter, EV charger or variable-speed drive, Type AC is not just unsuitable — it is unlawful to install.*

**Type A**
Detects sinusoidal AC and pulsating DC fault currents. This is the general type recommended by Amendment 2 and the default for:
- Single-phase solar inverters (grid-connect) — unless the inverter manual specifies Type B
- Most modern appliance circuits with switch-mode power supplies
- General residential circuits where electronics are connected

Type A is now the practical baseline for residential work, and it is the only permitted replacement for an existing Type AC device.

**Type F**
Detects sinusoidal AC, pulsating DC, and high-frequency leakage currents from variable-frequency drives. Required for:
- Air handling units with VFD-controlled fans
- Industrial machinery with variable-speed motor drives
- Some HVAC systems

Type F is uncommon in residential but increasingly relevant in commercial electrical work.

**Type B**
Detects all fault current types including smooth DC up to several kHz. Required where there is no other DC fault-current detection:
- EV chargers (EVSE) without a built-in 6mA RDC-DD
- Three-phase solar inverters where the manufacturer specifies Type B
- Battery storage systems with DC-connected inverters
- Any load with a rectifier bridge producing smooth DC output

| Application | Minimum RCD Type |
|---|---|
| Standard socket outlets (residential) | Type A |
| Lighting circuits | Type A |
| Single-phase solar inverter | Type A (check inverter specs — may require Type B) |
| Three-phase solar inverter | Type B where specified by the manufacturer |
| Battery storage (DC-coupled) | Type B where specified by the manufacturer |
| EV charger with integrated 6mA RDC-DD | Type A |
| EV charger without DC fault detection | Type B |
| Variable frequency drives | Type F or Type B |

**Practical rule:** When in doubt, specify Type B. The cost premium is modest compared to a failed audit or a warranty void from the equipment manufacturer.

---

## Switchboard Upgrades: When Does Full Retrofitting Apply?

This is the grey area that generates the most compliance questions.

**Full switchboard replacement:** Installing a new switchboard — removing the old board and fitting a new one — triggers full compliance with AS/NZS 3000:2018 on all circuits connected to that board. Every final sub-circuit must receive RCD protection compliant with the current standard.

**Adding new circuits to an existing board:** The new circuit must comply with AS/NZS 3000:2018, and Clause 2.6.3.2.5 requires RCD protection on any circuit that is altered or whose source of supply changes. Existing untouched circuits on the board are not automatically required to be upgraded.

**Where the line sits in practice:**

- Adding 1–2 new circuits: the new circuits need RCD protection; the rest of the board does not automatically
- Replacing the main switch, upgrading the incomer, or replacing all circuit protection on the board: Clause 2.6.3.2.5 treats this as triggering RCD protection for the final subcircuits supplied by that board
- Adding solar or a battery that back-feeds existing circuits: those circuits are "altered" because their source of supply has changed, so they need RCD protection

**Energy Safe Victoria's published position:** ESV's guidance on multiple-mode inverters and battery systems states that circuits connected to an alternative supply are deemed altered for the purposes of AS/NZS 3000, so Clause 2.6.3.2.5 applies and suitable RCD protection is required on those circuits — including the correct RCD type specified by the inverter manufacturer.

When uncertain, apply the current standard to the entire board. The cost of an RCD-per-circuit retrofit is orders of magnitude less than a failed inspection and remediation.

---

## State Variations in Enforcement

**Victoria (Energy Safe Victoria)**
ESV is the most active enforcer of AS/NZS 3000 technical requirements in Australia. Amendment 2 requirements have been incorporated into ESV's compliance framework. CES audit teams check RCD type compliance specifically on solar and battery installations.

**NSW (SafeWork NSW)**
Building Commission NSW administers the CCEW (Certificate of Compliance for Electrical Work) through BCNSW eCert — the certificate must be lodged there, not held as a PDF. CCEWs that certify work not meeting AS/NZS 3000 requirements expose the certifying electrician to prosecution under the Gas and Electricity (Consumer Safety) Act 2017. NSW audits of unlicensed or defective electrical work have increased since 2024.

**Queensland (Electrical Safety Office)**
ESO Queensland requires all electrical work to comply with the current edition of AS/NZS 3000. The ESO's audit program has specifically focused on solar installations with incorrect RCD types. Queensland does not use a "Form" for electrical compliance: the contractor must issue a **certificate of testing and compliance** for electrical installation work, and a certificate of testing and safety for work on electrical equipment, under the Electrical Safety Regulation — and keep a copy for five years.

---

## Testing Requirements: AS/NZS 3017

Installed RCDs must be tested for correct operation — Clause 8.3.10 of AS/NZS 3000 requires this for newly installed devices, and the test methods sit in **AS/NZS 3017 — Electrical Installations: Verification Guidelines**. Amendment 2 also added Clause 8.3.2.2, which recommends recording test results that produce a value rather than leaving them undocumented.

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
- Build CCEW and certificate of testing and compliance into your standard job close-out workflow

[Start your free ServiceM8 trial →](https://www.servicem8.com/?ref=tradieautomate&utm_source=tradieautomate&utm_medium=blog&utm_campaign=affiliate)

---

## FAQ

### Which circuits require RCD protection under AS/NZS 3000:2018?

Every final subcircuit in a domestic or residential installation — socket outlets, lighting and fixed equipment such as ovens, hot water and air conditioning — under Clause 2.6.3.2.2. This has been the rule since the 2018 edition replaced the 2007 edition, which only covered socket outlet circuits. Amendment 2 added the Type AC ban, not the lighting coverage.

### What RCD type do I need for a solar inverter installation?

Type A as the general choice for single-phase inverters, unless the inverter manual specifies Type B — in which case the manufacturer's requirement governs and Type A is a non-compliance. Always check the installation manual before specifying.

### What RCD type is required for an EV charger?

Either a Type B RCD, or a Type A RCD with a 6mA RDC-DD (built into most Mode 3 chargers to IEC 62955). Type AC is prohibited. Confirm with both the charger's installation documentation and your DNSP's technical standards.

### Does replacing a switchboard trigger full RCD compliance on all circuits?

Yes. A full switchboard replacement triggers RCD protection under Clause 2.6.3.2.5 for all final subcircuits supplied by that board. Adding circuits to an existing board requires the new or altered circuits to comply; untouched circuits are not automatically upgraded.

### What does "substantially altered" mean under AS/NZS 3000?

The standard does not use that phrase — it talks about alterations to an installation and replacement of switchboards (Clauses 2.6.3.2.5 and 1.4.8). What matters is whether a circuit has been altered or had its source of supply changed. When uncertain, apply the current standard to the whole board.

---


---

> **This article is featured in Chapter 2 of The Sparky's Playbook.**
> The free 12-chapter guide for Australian electricians — licensing, EV charging, commercial solar, cash flow, tech stack, and building a business worth selling.
> [Download the full book free →](/playbook)

---

## Related Reading

> **Checking what your state pays for upgrades?** If you're an electrician doing switchboard, heat-pump or solar work, the [Rebate & Incentives Finder](/tools/rebate-finder/) shows the current state rebates your customers qualify for — verified weekly against the regulator sources.

- *[Electrical Switchboard Upgrade Cost Australia 2026](/blog/electrical-switchboard-upgrade-cost-australia-2026/)*
- *[Solar Compliance Checklist for Australian Installers (2026)](/blog/solar-compliance-checklist-2026/)*
- *[Staying Compliant in 2026: The Complete Safety and Compliance Guide](/blog/staying-compliant-2026-solar-electrical-safety/)*
- *[CER Audit Prep: How to Pass Your Clean Energy Regulator Audit](/blog/cer-audit-prep-solar-installers/)*
- *[Commercial EV Charging Installation: The Electrician's Business Guide for 2026](/blog/commercial-ev-charging-installation-guide-electricians/)*
- *[EV Charger Installation Business Case for Electricians 2026](/blog/ev-charger-installation-business-case-electricians-2026/)*

