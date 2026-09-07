"""
Generate the free 1-page "Business Valuation Summary" PDF for the Tradie Business Value Calculator.
Static (not per-user) — the personalised estimate is delivered in the email body; this PDF is the
keepable reference explaining the method + next steps.

Design system matches the exit-readiness PDFs: orange top bar, navy headers, link cards, CTA box.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = A4

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

LEFT = 48
RIGHT = PAGE_W - 48
TEXT_WIDTH = RIGHT - LEFT
TOP = PAGE_H - 46
BOTTOM = 22
LEADING = 10.5
BODY_SIZE = 8.5

FONT = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'

SM8_URL = 'https://www.servicem8.com/?ref=tradieautomate&utm_source=tradieautomate&utm_medium=pdf&utm_campaign=business-value-calculator'
PLAYBOOK_URL = 'https://tradieautomate.com/playbook'


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


def draw_text_block(c, y, text, font_size=BODY_SIZE, color=BODY, width=TEXT_WIDTH, leading=LEADING):
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
        c.setFont(FONT, font_size)
        c.setFillColor(color)
        c.drawString(LEFT, y, line)
    return y


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
    c.linkURL(url, (text_x, card_cy - 2, text_x + tw, card_cy + 10), relative=0, thickness=0, color=LINK_BLUE)
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
    c.drawString(ix, cy, "Ready to systemise your business and lift the multiple?")
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


def build():
    out = '/Users/shane/tradieautomate/repo/public/business-valuation-summary.pdf'
    c = canvas.Canvas(out, pagesize=A4)
    draw_orange_bar(c)
    y = TOP

    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 18)
    c.drawString(LEFT, y, "Business Valuation Summary")
    y -= 21

    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 11)
    c.drawString(LEFT, y, "How Australian trade businesses are valued \u2014 and what yours is worth")
    y -= 16

    y = draw_text_block(c, y,
        "Trade businesses don't sell on revenue alone. A buyer looks at how much money the business "
        "actually makes for its owner \u2014 called Seller's Discretionary Earnings (SDE) \u2014 and applies "
        "a multiple to it. The multiple is where the money is: a business that runs on systems with "
        "predictable recurring revenue can sell for 2\u20133x SDE, while a paper-based, owner-dependent "
        "business often sells for just 1.2\u20131.8x.")
    y -= 4

    y = draw_navy_header(c, y, "THE VALUATION FORMULA")
    y = draw_text_block(c, y,
        "SDE \u2248 annual revenue \u00d7 net margin (trades run ~12\u201318%).  Value = SDE \u00d7 multiple.  "
        "The multiple scales with systems maturity:")
    y -= 4

    # Multiple table as clean text rows
    table_rows = [
        ("Paper / whiteboard, owner-dependent", "1.2 \u2013 1.8\u00d7"),
        ("Basic digital (accounting only)", "1.6 \u2013 2.2\u00d7"),
        ("Integrated (ServiceM8 / simPRO, staff-led)", "2.0 \u2013 3.0\u00d7"),
    ]
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(NAVY)
    c.drawString(LEFT, y, "SYSTEMS MATURITY")
    c.drawString(RIGHT - 60, y, "MULTIPLE")
    y -= 13
    for label, mult in table_rows:
        c.setFont(FONT, 8.5)
        c.setFillColor(BODY)
        c.drawString(LEFT, y, label)
        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(ORANGE)
        c.drawString(RIGHT - 60, y, mult)
        y -= 13
    y -= 2

    y = draw_navy_header(c, y, "YOUR NEXT 3 STEPS")
    steps = [
        ("1.  Know your SDE.", "Pull last year's net profit + your own drawings + one-off owner perks. That total is your SDE \u2014 the number buyers actually value."),
        ("2.  Lift the multiple.", "Every system you build (job workflows, compliance forms, recurring contracts) moves you up the multiple table. Systems are literally worth money at sale time."),
        ("3.  Get a professional read.", "This is an estimate for planning. Before any transaction, a licensed business valuer or M&A broker gives the defensible number."),
    ]
    for head, body in steps:
        y = draw_text_block(c, y, head, font_size=9, color=NAVY)
        y = draw_text_block(c, y, body)
        y -= 3

    # Disclaimer
    y -= 2
    c.setFillColor(HexColor('#718096'))
    c.setFont(FONT, 7)
    y = draw_text_block(c, y,
        "Estimate only \u2014 not a professional valuation, and not financial, legal or tax advice. "
        "Actual sale prices depend on the buyer, market conditions and due diligence.", font_size=7, color=HexColor('#718096'))
    y -= 4

    # Divider + continue reading
    c.setStrokeColor(LIGHT_GREY)
    c.setLineWidth(1)
    c.line(LEFT, y, RIGHT, y)
    y -= 8
    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 10)
    c.drawString(LEFT, y, "Continue Reading on TradieAutomate:")
    y -= 12
    links = [
        ("How to Sell Your ServiceM8-Based Trade Business for Maximum Value", "https://tradieautomate.com/blog/sell-servicem8-trade-business-value"),
        ("Exit-Readiness Quiz: Is Your Business Built to Sell?", "https://tradieautomate.com/exit-readiness"),
        ("Scaling a Solar & Electrical Business: Hiring, Systems and Growth", "https://tradieautomate.com/blog/scaling-solar-electrical-business-hiring-growth"),
    ]
    for i, (title, url) in enumerate(links):
        y = draw_link_card(c, y, title, url, num=i + 1)

    y -= 2
    y = draw_cta_box(c, y)

    # Playbook footer
    y -= 4
    c.setFillColor(BODY)
    c.setFont(FONT, 7.5)
    c.drawString(LEFT, y, "Want the full system? Download the free 12-chapter ")
    pb_text = "Sparky's Playbook"
    x_off = c.stringWidth("Want the full system? Download the free 12-chapter ", FONT, 7.5)
    c.setFillColor(LINK_BLUE)
    c.setFont(FONT_BOLD, 7.5)
    c.drawString(LEFT + x_off, y, pb_text)
    tw = c.stringWidth(pb_text, FONT_BOLD, 7.5)
    c.linkURL(PLAYBOOK_URL, (LEFT + x_off, y - 2, LEFT + x_off + tw, y + 8), relative=0, thickness=0, color=LINK_BLUE)
    c.setFillColor(BODY)
    c.setFont(FONT, 7.5)
    c.drawString(LEFT + x_off + tw, y, " \u2014 free.")

    # Page footer
    c.setFillColor(HexColor('#A0AEC0'))
    c.setFont(FONT, 6)
    c.drawCentredString(PAGE_W / 2, 18, "TradieAutomate.com \u2014 Business Valuation Summary")

    c.showPage()
    c.save()
    print("saved", out)


if __name__ == '__main__':
    build()
