---
title: "Solar & Battery System Components: Exploded View (Visual Guide)"
description: "See every component of a residential solar and battery system — panels, DC isolator, inverter, battery, AC isolator, switchboard and meter — and the AS/NZS standard governing each, in one clickable diagram."
pubDate: 2026-09-08
updatedDate: 2026-09-08
image: "/diagrams/solar-battery-system.svg"
imageAlt: "Exploded view of the seven components of a residential solar and battery system, from panels to meter, each tagged with its governing AS/NZS standard"
poster: "/diagrams/solar-battery-system.png"
aspectRatio: 1.7895
caption: "The seven components of a residential solar and battery system, pulled apart from the power flow. The tag in each header shows the AS/NZS standard that governs it. Tap any number to see what the component does and where installs commonly slip up."
hotspots:
  - id: solar-array
    label: "Solar array"
    note: "The panels on the roof that generate DC power. Governed by AS/NZS 5033:2021, which sets the array wiring, earthing and signage rules. Key points: DC cabling can't run within 600mm of the ceiling in most zones, and the main switchboard needs a system-layout sign showing how the array is isolated. Common mistake: missing the isolation-type signage (AC/DP/SW) that 5033 now requires."
    x: 9.41
    y: 39.21
    href: "/blog/staying-compliant-2026-solar-electrical-safety"
    hrefLabel: "Solar safety compliance →"
  - id: dc-isolator
    label: "DC isolator"
    note: "The load-break switch that safely cuts DC between the array and inverter. AS/NZS 5033:2021 requires it adjacent to (or integrated with) the inverter, rated to DCPV-2. For one or two parallel strings, a rooftop isolator is no longer required — the inverter-adjacent one is enough. Common mistake: undersizing the isolator for the array's voltage and current."
    x: 22.94
    y: 58.68
    href: "/blog/solar-compliance-checklist-2026"
    hrefLabel: "Compliance checklist →"
  - id: inverter
    label: "Inverter"
    note: "Converts DC to AC and (in a hybrid) manages the battery. Governed by AS/NZS 4777.2 for grid connection — a compliant inverter must support CSIP-AUS for smart export settings. Common mistake: installing an inverter that isn't on the CEC approved-products list, which voids the rebate and can fail inspection."
    x: 36.47
    y: 39.21
    href: "/blog/solar-warranty-claim-process-australia-2026"
    hrefLabel: "Inverter warranty guide →"
  - id: battery
    label: "Battery"
    note: "Stores DC energy, DC-coupled to the hybrid inverter. AS/NZS 5139:2019 controls where it can go: not within 600mm of an exit or entry point, and not within 600mm of a window or vent opening into a habitable room, plus fire-separation from neighbouring structures. Common mistake: mounting it too close to a door or window and failing inspection."
    x: 50.0
    y: 58.68
    href: "/blog/sparkys-playbook-chapter-6-battery-storage-systems-australia"
    hrefLabel: "Battery systems guide →"
  - id: ac-isolator
    label: "AC isolator"
    note: "The AC-side switch between inverter and switchboard, per AS/NZS 4777.1. Must be lockable and clearly labelled so the system can be safely isolated for maintenance. Common mistake: an unlabelled isolator that leaves the next electrician guessing where the solar feed isolates."
    x: 63.53
    y: 39.21
  - id: switchboard
    label: "Switchboard"
    note: "Where solar meets the home's wiring under AS/NZS 3000 (the Wiring Rules). Needs a dedicated solar circuit breaker plus RCD protection, and a solar-supply label. Common mistake: putting the solar breaker on the wrong side of the RCD, or skipping the label that inspectors look for."
    x: 77.06
    y: 58.68
    href: "/blog/sparkys-playbook-chapter-2-safety-standards-as-nzs-3000-electricians-australia"
    hrefLabel: "AS/NZS 3000 wiring rules →"
  - id: meter
    label: "Meter"
    note: "The point where the system connects to the grid and exports excess power. The export limit is set by your distributor (DNSP) — it varies by network and connection type, so always check the DNSP's connection page before quoting. Common mistake: assuming a universal export limit, then having the distributor knock the system back."
    x: 90.59
    y: 39.21
    href: "/blog/vic-solar-connection-guide-2026"
    hrefLabel: "Grid connection guide →"
cta:
  text: "Get the complete compliance reference for every component in this system — AS/NZS 5033, 5139, 4777 and 3000 in one printable checklist."
  href: "/compliance-checklist"
  label: "Download the Solar Compliance Checklist →"
faq:
  - question: "What are the main components of a solar and battery system?"
    answer: "A residential hybrid system has seven core components: the solar array (panels), a DC isolator, the inverter (which converts DC to AC and manages the battery), the battery itself, an AC isolator, the switchboard, and the meter/grid connection. The DC isolator, inverter, battery, AC isolator and switchboard are each governed by a specific AS/NZS standard — 5033, 4777.2, 5139, 4777.1 and 3000 respectively."
  - question: "What is the difference between a DC and AC isolator?"
    answer: "A DC isolator sits on the DC side between the solar array and the inverter, cutting the direct current from the panels (governed by AS/NZS 5033). An AC isolator sits between the inverter and the switchboard, cutting the alternating current feeding the home (governed by AS/NZS 4777.1). Both are load-break safety switches, but they isolate different sides of the system and have different ratings."
  - question: "Where can a home battery be installed under AS/NZS 5139?"
    answer: "AS/NZS 5139:2019 restricts battery placement for fire safety. A battery must not be installed within 600mm of an exit or entry point, or within 600mm of a window or vent opening into a habitable room. Additional fire-separation distances apply to neighbouring structures and property boundaries. These restricted zones are the most common reason a battery installation fails inspection."
  - question: "What does an inverter's AS/NZS 4777.2 compliance mean?"
    answer: "AS/NZS 4777.2 is the standard for inverter grid connection. A compliant inverter must support CSIP-AUS, the Australian protocol for smart export settings, which lets the network remotely manage export limits. The inverter must also be on the Clean Energy Council's approved-products list to qualify for STC rebates and pass grid-connection approval."
  - question: "What determines my solar export limit?"
    answer: "Your export limit is set by your local distributor (DNSP), not a fixed national figure. It varies by network, connection type and whether the system is single or three phase. Always check the DNSP's connection requirements page before quoting a system, because an export limit lower than the customer expects can change the system design and payback."
---

Most tradies understand a solar and battery install as a physical system — panels on the roof, gear on the wall, power flowing through. This exploded-view diagram pulls that system apart so you can see every component, the order power flows through it, and the standard that governs each one.

The solid line through the middle is the **power flow** — DC on the left (from the panels and battery), converted to AC at the inverter, then out through the switchboard and meter to the grid. The dashed lines show each component pulled out from that flow. The tag in each header shows the AS/NZS standard that governs that component.

## How to Read This Diagram

- **The spine** is the power flow. Power moves left to right: DC from the panels and battery, converted to AC at the inverter, then through the switchboard and meter.
- **The DC side** (left) is the array, DC isolator, inverter and battery — governed by AS/NZS 5033 and 5139.
- **The AC side** (right) is the AC isolator, switchboard and meter — governed by AS/NZS 4777.1 and 3000.
- **The header tag** on each component shows the standard you need to meet. Tap any number to see the full explanation and where installs commonly slip up.

## Where Compliance Actually Bites

Four components cause most failed inspections, in order:

1. **Battery placement** — AS/NZS 5139 restricted zones (600mm from exits and habitable-room openings) catch installers out more than anything else.
2. **DC isolator sizing** — undersized isolators for the array's voltage and current are a recurring AS/NZS 5033 failure.
3. **Signage** — 5033 now requires isolation-type signage (AC/DP/SW) and a system-layout sign at the main switchboard.
4. **Export limit** — assuming a universal export limit instead of checking the DNSP leads to systems getting knocked back at connection.

The inverter is also worth checking against the CEC approved-products list before quoting — a non-approved inverter voids the STC rebate.

## Related Reading

- [Solar Compliance Checklist 2026](/blog/solar-compliance-checklist-2026)
- [Staying Compliant: Solar & Electrical Safety 2026](/blog/staying-compliant-2026-solar-electrical-safety)
- [Solar Battery System Cost Australia 2026](/blog/solar-battery-system-cost-australia-2026)
- [The Sparky's Playbook — Chapter 6: Battery Storage Systems](/blog/sparkys-playbook-chapter-6-battery-storage-systems-australia)
- [The Sparky's Playbook — Chapter 2: AS/NZS 3000 Safety Standards](/blog/sparkys-playbook-chapter-2-safety-standards-as-nzs-3000-electricians-australia)
