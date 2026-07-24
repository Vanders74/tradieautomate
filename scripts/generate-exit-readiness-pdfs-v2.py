"""
Generate all 3 Exit-Readiness Action Plan PDFs using reportlab.
Replaces the old fpdf-based generate-exit-readiness-pdfs.py.

Tiers:
  - high-risk:  85% gauge, orange subtitle, key-person dependency focus
  - scaling-trap: 55% gauge, amber subtitle, bottleneck focus
  - exit-ready:  15% gauge, green subtitle, maximising-multiple focus

Design system: orange top bar, navy section headers, compact risk gauge,
blue underlined link cards, CTA box, playbook footer. All clean URLs.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = A4

# Brand
ORANGE = HexColor('#E87722')
NAVY = HexColor('#1B2A4A')
LINK_BLUE = HexColor('#1a56db')
BODY = HexColor('#2D3748')
CREAM_BG = HexColor('#FDFAF5')
WHITE = white
LIGHT_GREY = HexColor('#EDF2F7')
CARD_BG = HexColor('#F7FAFC')
CARD_BORDER = HexColor('#E2E8F0')
GREEN_RESULT = HexColor('#276749')
GREY_URL = HexColor('#718096')
GAUGE_BG = HexColor('#E5E7EB')

# Layout
LEFT = 48
RIGHT = PAGE_W - 48
TEXT_WIDTH = RIGHT - LEFT
TOP = PAGE_H - 46
BOTTOM = 22
LEADING = 10.5
BODY_SIZE = 8.5

FONT = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'

# ServiceM8 affiliate URL
SM8_URL = 'https://www.servicem8.com/?ref=tradieautomate&utm_source=tradieautomate&utm_medium=pdf&utm_campaign=exit-readiness-quiz'
PLAYBOOK_URL = 'https://tradieautomate.com/playbook'


# ── Drawing helpers ──────────────────────────────────────────────

def draw_orange_bar(c):
    c.setFillColor(ORANGE)
    c.rect(0, PAGE_H - 14, PAGE_W, 14, fill=1, stroke=0)


def draw_navy_header(c, y, text):
    bar_h = 15
    c.setFillColor(NAVY)
    c.rect(LEFT, y - bar_h, TEXT_WIDTH, bar_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 8.5)
    c.drawString(LEFT + 8, y - bar_h + 4, text)
    return y - bar_h - 3


def draw_text_block(c, y, text, font_size=BODY_SIZE, color=BODY, width=TEXT_WIDTH,
                    leading=LEADING, bold_phrases=None):
    words = text.split()
    lines = []
    cur_line = []
    cur_w = 0
    for word in words:
        c.setFont(FONT, font_size)
        w = c.stringWidth(word + ' ', FONT, font_size)
        if cur_w + w > width and cur_line:
            lines.append(' '.join(cur_line))
            cur_line = [word]
            cur_w = c.stringWidth(word + ' ', FONT, font_size)
        else:
            cur_line.append(word)
            cur_w += w
    if cur_line:
        lines.append(' '.join(cur_line))
    for line in lines:
        y -= leading
        if y < BOTTOM:
            break
        if bold_phrases:
            _draw_rich(c, LEFT, y, line, font_size, color, bold_phrases)
        else:
            c.setFont(FONT, font_size)
            c.setFillColor(color)
            c.drawString(LEFT, y, line)
    return y


def _draw_rich(c, x, y, line, font_size, color, phrases):
    remaining = line
    px = x
    while remaining:
        earliest = len(remaining)
        earliest_p = None
        for p in phrases:
            pos = remaining.lower().find(p.lower())
            if pos != -1 and pos < earliest:
                earliest = pos
                earliest_p = p
        if earliest_p is None:
            c.setFont(FONT, font_size)
            c.setFillColor(color)
            c.drawString(px, y, remaining)
            break
        if earliest > 0:
            c.setFont(FONT, font_size)
            c.setFillColor(color)
            before = remaining[:earliest]
            c.drawString(px, y, before)
            px += c.stringWidth(before, FONT, font_size)
        c.setFont(FONT_BOLD, font_size)
        c.setFillColor(color)
        phrase_in = remaining[earliest:earliest + len(earliest_p)]
        c.drawString(px, y, phrase_in)
        px += c.stringWidth(phrase_in, FONT_BOLD, font_size)
        remaining = remaining[earliest + len(earliest_p):]


def draw_gauge(c, y, pct, risk_color, risk_label):
    """Compact single-line risk gauge. pct is 0-100, risk_color is the label color."""
    label = "Key-Person Dependency:"
    c.setFillColor(BODY)
    c.setFont(FONT_BOLD, 8.5)
    c.drawString(LEFT, y, label)
    label_w = c.stringWidth(label + " ", FONT_BOLD, 8.5)

    bar_x = LEFT + label_w
    bar_w = 180
    bar_h = 8
    bar_y = y - 1

    # Background
    c.setFillColor(GAUGE_BG)
    c.setStrokeColor(HexColor('#D1D5DB'))
    c.setLineWidth(0.3)
    c.roundRect(bar_x, bar_y, bar_w, bar_h, 2, fill=1, stroke=1)

    # Three segments: green, amber, red
    seg = bar_w / 3.0
    c.setFillColor(HexColor('#10B981'))
    c.rect(bar_x, bar_y, seg, bar_h, fill=1, stroke=0)
    c.setFillColor(HexColor('#F59E0B'))
    c.rect(bar_x + seg, bar_y, seg, bar_h, fill=1, stroke=0)
    c.setFillColor(HexColor('#DC2626'))
    c.rect(bar_x + seg * 2, bar_y, seg, bar_h, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#D1D5DB'))
    c.roundRect(bar_x, bar_y, bar_w, bar_h, 2, fill=0, stroke=1)

    # White marker
    marker_x = bar_x + bar_w * (pct / 100.0)
    c.setStrokeColor(WHITE)
    c.setLineWidth(1.5)
    c.line(marker_x, bar_y + 1.5, marker_x, bar_y + bar_h - 1.5)

    # Score
    score_x = bar_x + bar_w + 8
    c.setFillColor(risk_color)
    c.setFont(FONT_BOLD, 8.5)
    c.drawString(score_x, y, f"{pct}%")
    score_w = c.stringWidth(f"{pct}% ", FONT_BOLD, 8.5)
    c.setFont(FONT_BOLD, 7.5)
    c.drawString(score_x + score_w, y, risk_label)

    return y - 10


def draw_link_card(c, y, title, url, num=None):
    card_h = 18
    card_y = y - card_h
    c.setFillColor(CARD_BG)
    c.setStrokeColor(CARD_BORDER)
    c.setLineWidth(0.4)
    c.roundRect(LEFT, card_y, TEXT_WIDTH, card_h, 3, fill=1, stroke=1)

    text_x = LEFT + 10
    card_cy = card_y + card_h / 2
    if num:
        c.setFillColor(ORANGE)
        c.circle(LEFT + 13, card_cy, 6.5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 6.5)
        c.drawCentredString(LEFT + 13, card_cy - 2.5, str(num))
        text_x = LEFT + 26

    c.setFillColor(LINK_BLUE)
    c.setFont(FONT_BOLD, 8.5)
    c.drawString(text_x, card_cy + 3, title)
    tw = c.stringWidth(title, FONT_BOLD, 8.5)
    c.setStrokeColor(LINK_BLUE)
    c.setLineWidth(0.5)
    c.line(text_x, card_cy + 1.5, text_x + tw, card_cy + 1.5)
    c.linkURL(url, (text_x, card_cy - 2, text_x + tw, card_cy + 10),
              relative=0, thickness=0, color=LINK_BLUE)

    return y - card_h - 6


def draw_cta_box(c, y):
    box_h = 41
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.5)
    c.setFillColor(CREAM_BG)
    c.roundRect(LEFT, y - box_h, TEXT_WIDTH, box_h, 5, fill=1, stroke=1)

    ix = LEFT + 14
    cy = y - 12
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 10)
    c.drawString(ix, cy, "Ready to systemise your business?")
    cy -= 14

    cta = "Start your free 14-day ServiceM8 trial \u2192"
    c.setFillColor(LINK_BLUE)
    c.setFont(FONT_BOLD, 9)
    c.drawString(ix, cy, cta)
    tw = c.stringWidth(cta, FONT_BOLD, 9)
    c.setStrokeColor(LINK_BLUE)
    c.setLineWidth(0.5)
    c.line(ix, cy - 1.5, ix + tw, cy - 1.5)
    c.linkURL(SM8_URL, (ix, cy - 2, ix + tw, cy + 9), relative=0, thickness=0, color=LINK_BLUE)
    cy -= 10

    c.setFillColor(BODY)
    c.setFont(FONT, 7.5)
    c.drawString(ix, cy, "14-day free trial. No credit card. Unlimited staff.")
    return y - box_h - 4


def draw_playbook_footer(c, y):
    c.setFillColor(BODY)
    c.setFont(FONT, 7.5)
    c.drawString(LEFT, y,
        "This action plan is a starting point. For the complete 12-chapter system covering "
        "licensing, cash flow, tech stack, hiring, and building a business worth selling \u2014")
    y -= 9
    c.drawString(LEFT, y, "download ")
    pb_text = "The Sparky's Playbook"
    x_off = c.stringWidth("download ", FONT, 7.5)
    c.setFillColor(LINK_BLUE)
    c.setFont(FONT_BOLD, 7.5)
    c.drawString(LEFT + x_off, y, pb_text)
    tw = c.stringWidth(pb_text, FONT_BOLD, 7.5)
    c.setStrokeColor(LINK_BLUE)
    c.setLineWidth(0.5)
    c.line(LEFT + x_off, y - 1.5, LEFT + x_off + tw, y - 1.5)
    c.linkURL(PLAYBOOK_URL, (LEFT + x_off, y - 2, LEFT + x_off + tw, y + 8),
              relative=0, thickness=0, color=LINK_BLUE)
    c.setFillColor(BODY)
    c.setFont(FONT, 7.5)
    c.drawString(LEFT + x_off + tw, y, " (free)")
    return y - 10


# ── Action + result block ─────────────────────────────────────────

def draw_action(c, y, num, heading, body_text, result_text):
    """Draw one action item: orange heading, body, green result. Returns new Y."""
    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 10)
    c.drawString(LEFT, y, f"{num}.  {heading}")
    y -= 18

    y = draw_text_block(c, y, body_text)
    y -= 5

    rtext = f"\u2192 Result: {result_text}"
    y = draw_text_block(c, y, rtext, color=GREEN_RESULT, bold_phrases=["\u2192 Result:"])
    return y


# ── Common page shell ─────────────────────────────────────────────

def build_page(c, tier):
    """
    tier = {
        'subtitle': str,
        'subtitle_color': HexColor,
        'gauge_pct': int,
        'gauge_color': HexColor,
        'gauge_label': str,
        'intro': str,
        'intro_bold': str or None,
        'diagnosis': str,
        'actions': [(heading, body, result), ...],
        'links': [(title, url), ...],
    }
    """
    draw_orange_bar(c)
    y = TOP

    # Title
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 18)
    c.drawString(LEFT, y, "Exit-Readiness Action Plan")
    y -= 21

    # Subtitle
    c.setFillColor(tier['subtitle_color'])
    c.setFont(FONT_BOLD, 11)
    c.drawString(LEFT, y, tier['subtitle'])
    y -= 14

    # Gauge
    y = draw_gauge(c, y, tier['gauge_pct'], tier['gauge_color'], tier['gauge_label'])
    y -= 8

    # Intro
    y = draw_text_block(c, y, tier['intro'])
    if tier.get('intro2'):
        bp = [tier['intro_bold']] if tier.get('intro_bold') else None
        y = draw_text_block(c, y, tier['intro2'], bold_phrases=bp)
    y -= 4

    # Destination (same aspirational copy for all tiers)
    y = draw_navy_header(c, y, "THE DESTINATION: WHAT A SYSTEMISED BUSINESS FEELS LIKE")
    dest = (
        "Picture this. It's a Tuesday morning in January. You're at the beach with your kids. "
        "Your phone stays in your pocket \u2014 the jobs are scheduled, the crew knows exactly "
        "what to do, compliance certificates are filing themselves, and invoices are going out "
        "at job completion. Nobody is calling because nobody needs to. The business is running "
        "on systems \u2014 not on you. When the time comes to sell, a buyer looks at your "
        "operation and sees a well-oiled machine: documented workflows, predictable margins, "
        "a trained team, and a business that doesn't miss a beat whether the owner is in the "
        "office or on a plane to Bali. They pay a premium because they're buying a business, "
        "not a job. Electrical contractors just like you make this transition every year. "
        "The ones who succeed all do three things."
    )
    y = draw_text_block(c, y, dest)
    y -= 4

    # Diagnosis
    y = draw_navy_header(c, y, "YOUR DIAGNOSIS")
    y = draw_text_block(c, y, tier['diagnosis'])
    y -= 4

    # Actions
    y = draw_navy_header(c, y, "YOUR TOP 3 PRIORITY ACTIONS (AND THE RESULT YOU GET)")
    y -= 8

    for i, (heading, body, result) in enumerate(tier['actions']):
        y = draw_action(c, y, i + 1, heading, body, result)
        y -= 10  # generous gap between actions

    # Divider
    c.setStrokeColor(LIGHT_GREY)
    c.setLineWidth(1)
    c.line(LEFT, y, RIGHT, y)
    y -= 8

    # Continue Reading
    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 10)
    c.drawString(LEFT, y, "Continue Reading on TradieAutomate:")
    y -= 12

    for i, (title, url) in enumerate(tier['links']):
        y = draw_link_card(c, y, title, url, num=i + 1)

    y -= 2

    # CTA
    y = draw_cta_box(c, y)
    y -= 4

    # Playbook
    y = draw_playbook_footer(c, y)
    y -= 12

    # Page footer
    c.setFillColor(HexColor('#A0AEC0'))
    c.setFont(FONT, 6)
    c.drawCentredString(PAGE_W / 2, 18,
        "TradieAutomate.com \u2014 Exit-Readiness Action Plan \u2014 Page 1")


# ── Tier definitions ──────────────────────────────────────────────

TIERS = {
    'high-risk': {
        'subtitle': "High Key-Person Risk \u2014 Your Business Is a Job, Not an Asset",
        'subtitle_color': ORANGE,
        'gauge_pct': 85,
        'gauge_color': HexColor('#DC2626'),
        'gauge_label': "HIGH RISK",
        'intro': (
            "You built a successful electrical contracting business. But somewhere along the way, "
            "the business started running you instead of the other way around. You're the senior "
            "sparkie, the quoting department, the compliance officer, and the person who fields "
            "every crisis call \u2014 every single day. You can't take a holiday without the phone "
            "ringing. You can't get sick without jobs stalling. And deep down, you know that if "
            "you tried to sell tomorrow, a buyer would see a job \u2014 not a business worth paying "
            "a premium for."
        ),
        'intro2': (
            "Your quiz results confirm what you already feel: your business depends entirely on "
            "you. Buyers see this and discount heavily \u2014 or walk away entirely. The good news? "
            "Every problem the quiz identified has a specific fix. Better news: the destination "
            "is closer than you think."
        ),
        'intro_bold': "Your quiz results confirm what you already feel:",
        'diagnosis': (
            "Your business is currently a job, not a sellable asset. It relies on your time, "
            "energy, and personal memory. Quoting happens in your head. Compliance paperwork "
            "lives in WhatsApp. If you took a month off, the business would stall \u2014 because "
            "the system IS you. Buyers buy systems, not people. The fix starts with three things: "
            "get off the tools, centralise your pricing, and build job workflows that don't depend "
            "on you being there. Every one of these is achievable in 3\u20136 months with the right "
            "software \u2014 and the result is a business that works for you, not the other way around."
        ),
        'actions': [
            (
                "Centralise your quoting rules and pricing",
                "Stop building quotes from memory \u2014 that's how margins leak. Set up standardised "
                "pricing templates with pre-loaded supplier costs, labour rates, and margin targets "
                "in ServiceM8. When every quote follows the same rules, you stop being the bottleneck, "
                "and you stop leaving money on the table.",
                "You win jobs at the right margin without touching a calculator. Your team quotes consistently \u2014 whether you're in the office or on holiday."
            ),
            (
                "Build systemised SOPs in ServiceM8",
                "Every job type needs a documented workflow: what happens at booking, what forms "
                "are required on site, what photos must be captured, and what sign-off steps close "
                "the job. Build these once in ServiceM8, and every technician \u2014 including ones "
                "you haven't hired yet \u2014 follows the same process.",
                "Your business runs the same whether you're there or not. New hires hit the ground running. Compliance is never a last-minute panic."
            ),
            (
                "Track job profitability per job type",
                "You can't fix margins you can't see. Connect ServiceM8 to Xero or MYOB so labour "
                "hours and supplier costs are tracked against every job in real time. Within 3 months, "
                "you'll know exactly which job types make money and which are quietly bleeding it.",
                "You stop doing unprofitable work. Every job you take contributes to your bottom line \u2014 and to your eventual sale price."
            ),
        ],
        'links': [
            ("ServiceM8 for Electricians \u2014 Full Guide",
             "https://tradieautomate.com/blog/servicem8-for-electricians"),
            ("How to Sell Your ServiceM8-Based Trade Business",
             "https://tradieautomate.com/blog/sell-servicem8-trade-business-value"),
            ("Hidden Costs Killing Your Profit as a Solar Installer or Electrician",
             "https://tradieautomate.com/blog/hidden-costs-killing-profit-solar-electrician"),
        ],
    },

    'scaling-trap': {
        'subtitle': "The Scaling Trap \u2014 You've Grown, But You're Still the Bottleneck",
        'subtitle_color': HexColor('#D97706'),
        'gauge_pct': 55,
        'gauge_color': HexColor('#D97706'),
        'gauge_label': "MODERATE RISK",
        'intro': (
            "You've built a real business with a team, revenue, and customers. But you're still "
            "the pin in every process \u2014 the one who approves quotes, chases compliance paperwork, "
            "and puts out fires. Buyers see real potential here, but they'll discount for the "
            "key-person risk. You're not a job anymore, but you're not yet a sellable asset. "
            "The good news: you're closer than you think. Fix the bottlenecks and your valuation "
            "multiple jumps."
        ),
        'intro2': None,
        'intro_bold': None,
        'diagnosis': (
            "You've grown beyond a solo operation, but you're the operational bottleneck. You have "
            "basic systems in place \u2014 maybe Xero for accounting, some checklists for the crew \u2014 "
            "but you lack the automation to remove yourself from day-to-day admin, compliance chasing, "
            "and job costing. The scaling trap is common: the business grew faster than the systems. "
            "The fix isn't working harder \u2014 it's connecting the tools you already have so they "
            "talk to each other without you in the middle. Every one of these is achievable in "
            "3\u20136 months with the right software."
        ),
        'actions': [
            (
                "Automate compliance documentation so jobs close without you",
                "Right now you're chasing technicians for missing photos, blurry serial numbers, and "
                "unsigned CCEW forms. ServiceM8's digital job forms make compliance mandatory \u2014 "
                "jobs can't be marked complete until all checks pass automated validation. The Friday "
                "afternoon paperwork scramble disappears.",
                "Jobs close on-site, not at 9 PM from your kitchen table. Compliance is verified automatically \u2014 no more chasing, no more gaps."
            ),
            (
                "Build recurring revenue streams",
                "Zero recurring revenue is the single biggest drag on your valuation multiple. Start "
                "converting one-off clients into maintenance contracts, annual inspection agreements, "
                "and monitoring subscriptions. Even 10\u201315% recurring revenue can add 0.5\u20131x "
                "to your EBIT multiple. ServiceM8's scheduling engine handles recurring job creation "
                "automatically.",
                "Every maintenance contract you add is directly increasing your eventual sale price. Predictable monthly revenue \u2014 predictable exit."
            ),
            (
                "Integrate your tech stack end-to-end",
                "You have the pieces \u2014 accounting software, maybe some scheduling tools \u2014 but "
                "they don't talk to each other. Connect ServiceM8 to Xero or MYOB so invoices, payments, "
                "and client records sync automatically. One source of truth. No double-entry. Live job "
                "profitability at your fingertips.",
                "You stop being the human API between your tools. Your systems run the business while you run the strategy."
            ),
        ],
        'links': [
            ("ServiceM8 Review 2026 \u2014 Pricing, Features & Who It Suits",
             "https://tradieautomate.com/blog/servicem8-review-2026"),
            ("How to Sell Your ServiceM8-Based Trade Business",
             "https://tradieautomate.com/blog/sell-servicem8-trade-business-value"),
            ("Solar Monitoring & After-Sales Revenue Guide",
             "https://tradieautomate.com/blog/solar-monitoring-after-sales-revenue-australia"),
        ],
    },

    'exit-ready': {
        'subtitle': "Exit-Ready Asset \u2014 Your Business Is Built to Sell",
        'subtitle_color': HexColor('#16A34A'),
        'gauge_pct': 15,
        'gauge_color': HexColor('#16A34A'),
        'gauge_label': "LOW RISK",
        'intro': (
            "Your business has the systems, documentation, and management layer that buyers pay "
            "a premium for. Low key-person risk, automated compliance, real-time margin visibility \u2014 "
            "this is exactly what acquirers want to see. You've done the hard work of building a "
            "sellable asset. Now it's about maximising that multiple and preparing the transition "
            "so you walk away with the result you deserve."
        ),
        'intro2': None,
        'intro_bold': None,
        'diagnosis': (
            "You've successfully decoupled your time from business revenue. Low key-person risk, "
            "automated compliance, real-time margin visibility, and a management layer that runs "
            "without you \u2014 this is exactly what buyers want to see. Your business is an attractive, "
            "high-multiple acquisition target. At this stage, the work shifts from building systems "
            "to optimising for exit: maximising recurring revenue, getting a professional valuation, "
            "and preparing the leadership transition plan that lets you walk away clean."
        ),
        'actions': [
            (
                "Maximise recurring revenue to boost your EBIT multiple",
                "Every percentage point of recurring revenue \u2014 maintenance contracts, monitoring "
                "subscriptions, service agreements \u2014 adds measurable value to your exit multiple. "
                "A business with 20%+ recurring revenue can command 3\u20134x EBIT vs 2\u20132.5x for "
                "comparable project-only businesses. ServiceM8's scheduling engine makes recurring "
                "job management automatic.",
                "The difference between 15% and 25% recurring revenue could be hundreds of thousands at exit. Every contract you add now pays twice \u2014 once in cash flow, once in sale price."
            ),
            (
                "Get a professional valuation to benchmark your exit number",
                "Engage a business broker with specific trade business experience. They'll assess "
                "your ServiceM8 records, financials, customer concentration, and growth trajectory "
                "to establish a defensible valuation. Knowing your number lets you negotiate from "
                "strength and identify gaps before a buyer does.",
                "You walk into negotiations with data, not hope. A professional valuation is your anchor \u2014 buyers can't lowball what's been independently verified."
            ),
            (
                "Prepare your 3-year transition plan for leadership and key accounts",
                "Even an exit-ready business needs a handover. Document the transition timeline: "
                "when key accounts get introduced to new management, when supplier relationships "
                "transfer, when you step back from daily operations. A clean 12\u201336 month transition "
                "plan is the difference between a good exit and a great one.",
                "You exit on your terms, on your timeline. The business transfers smoothly, key relationships stay intact, and you walk away with the full value you built."
            ),
        ],
        'links': [
            ("How to Sell Your ServiceM8-Based Trade Business for Maximum Value",
             "https://tradieautomate.com/blog/sell-servicem8-trade-business-value"),
            ("The Modern Trade Tech Stack \u2014 Chapter 8 of The Sparky's Playbook",
             "https://tradieautomate.com/blog/sparkys-playbook-chapter-8-trade-tech-stack-job-management-accounting"),
            ("Scaling Your Electrical Business \u2014 Chapter 11",
             "https://tradieautomate.com/blog/sparkys-playbook-chapter-11-scaling-electrical-business-australia"),
        ],
    },
}


# ── Build all ─────────────────────────────────────────────────────

def generate_all(output_dir):
    import os
    os.makedirs(output_dir, exist_ok=True)

    for slug, tier in TIERS.items():
        filename = f"exit-readiness-plan-{slug}.pdf"
        path = os.path.join(output_dir, filename)
        c = canvas.Canvas(path, pagesize=A4)
        build_page(c, tier)
        c.save()
        print(f"Saved: {path}")


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
    generate_all(out)
