"""
Generate the paid "Tradie Business Valuation Report" — the Layer 2 product ($49, 100% margin).
Delivered via Payhip (merchant-of-record), so the output goes OUTSIDE the repo (not public/).
Multi-page deep guide using reportlab Platypus.

Output: /Users/shane/tradieautomate/products/full-valuation-report.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, HRFlowable, KeepTogether)

OUT = '/Users/shane/tradieautomate/products/full-valuation-report.pdf'

# Brand palette
ORANGE = HexColor('#E87722')
NAVY = HexColor('#1B2A4A')
LINK_BLUE = HexColor('#1a56db')
BODY = HexColor('#2D3748')
MUTED = HexColor('#718096')
LIGHT = HexColor('#F7FAFC')
BORDER = HexColor('#E2E8F0')

styles = {
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=24, leading=30, textColor=NAVY),
    'subtitle': ParagraphStyle('subtitle', fontName='Helvetica-Bold', fontSize=13, leading=18, textColor=ORANGE),
    'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=15, leading=20, textColor=NAVY, spaceBefore=14, spaceAfter=6),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=ORANGE, spaceBefore=10, spaceAfter=4),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=14, textColor=BODY, spaceAfter=7),
    'small': ParagraphStyle('small', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=MUTED, spaceAfter=5),
    'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.5, leading=14, textColor=BODY, leftIndent=14, bulletIndent=4, spaceAfter=4),
    'callout': ParagraphStyle('callout', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=NAVY),
}

def P(text, style='body'):
    return Paragraph(text, styles[style])

def B(text):
    return Paragraph(text, styles['bullet'], bulletText='\u2022')

def header_footer(canvas, doc):
    canvas.saveState()
    # Top orange bar
    canvas.setFillColor(ORANGE)
    canvas.rect(0, A4[1] - 14, A4[0], 14, fill=1, stroke=0)
    # Footer
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0]/2, 18, 'TradieAutomate \u00b7 Tradie Business Valuation Report \u00b7 Page %d' % doc.page)
    canvas.drawString(24, 18, 'tradieautomate.com')
    canvas.restoreState()

def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=24*mm, rightMargin=24*mm,
                            topMargin=20*mm, bottomMargin=18*mm,
                            title='Tradie Business Valuation Report', author='TradieAutomate')
    E = []

    # ── Cover ──
    E.append(Spacer(1, 40))
    E.append(P('TRADIE BUSINESS VALUATION REPORT', 'title'))
    E.append(Spacer(1, 8))
    E.append(P('What your Australian trade business is worth in 2026 \u2014 and the levers that increase it.', 'subtitle'))
    E.append(Spacer(1, 20))
    E.append(HRFlowable(width='100%', thickness=1.2, color=ORANGE))
    E.append(Spacer(1, 16))
    E.append(P('This report explains exactly how buyers value trade businesses, the multiple they apply to your '
               'earnings, and the specific changes that move that multiple. It is written for owners of electrical, '
               'solar, HVAC, plumbing and related trade businesses in Australia.'))
    E.append(Spacer(1, 10))
    E.append(P('<b>What you\u2019ll get:</b> the SDE valuation method in plain terms, 2026 benchmark multiples, the 7 value '
               'drivers, a buyer-readiness scorecard, a 90-day value-building plan, and the documents buyers will ask for.', 'body'))
    E.append(Spacer(1, 10))
    E.append(Paragraph('<i>Estimate &amp; education only \u2014 not a professional valuation, and not financial, legal or tax advice.</i>', styles['small']))
    E.append(PageBreak())

    # ── 1. The method ──
    E.append(P('1. How Trade Businesses Are Actually Valued', 'h1'))
    E.append(P('Most owners assume their business is worth a multiple of revenue. It isn\u2019t. Buyers buy <b>earnings</b>, and '
               'in small business the relevant earnings number is <b>Seller\u2019s Discretionary Earnings (SDE)</b>.'))
    E.append(P('<b>SDE = net profit + owner\u2019s salary + owner perks + one-off expenses.</b> It answers one question: '
               '\u201cHow much money does this business put in the owner\u2019s pocket each year?\u201d A buyer doesn\u2019t care about your '
               'headline revenue \u2014 they care about what they could earn from it.'))
    E.append(Spacer(1, 4))
    E.append(P('The valuation formula:', 'callout'))
    E.append(P('<b>Business value = SDE \u00d7 multiple</b>'))
    E.append(P('For Australian trade businesses, SDE is typically <b>12\u201318% of revenue</b> (the higher the better, driven by '
               'margins and how efficiently the business runs). The multiple is where most of the variance lives \u2014 and it\u2019s '
               'the part you can actually influence.'))
    E.append(P('Why this matters: two businesses with the same $1M revenue can be worth wildly different amounts. One runs '
               'on the owner\u2019s memory and whiteboard; the other runs on systems and recurring contracts. The first might '
               'sell for $150K. The second, $400K+. Same revenue. The difference is the multiple \u2014 and the multiple is '
               'bought with systems, not sales.'))
    E.append(PageBreak())

    # ── 2. The multiple ──
    E.append(P('2. The Multiple: What Buyers Actually Pay', 'h1'))
    E.append(P('The multiple applied to SDE scales with one thing: <b>how transferable the business is</b>. A buyer will pay a '
               'premium for a business that runs without the owner, and discount a business that is the owner.'))
    E.append(Spacer(1, 6))
    t = Table([
        [Paragraph('<b>Systems maturity</b>', styles['callout']), Paragraph('<b>Typical multiple</b>', styles['callout']), Paragraph('<b>What it means</b>', styles['callout'])],
        ['Paper / whiteboard, owner-dependent', '1.2 \u2013 1.8\u00d7', 'Owner is the quoting, compliance and dispatch department. Buyer buys a job, not a business.'],
        ['Basic digital (accounting only)', '1.6 \u2013 2.2\u00d7', 'Xero/MYOB in place, some processes, but owner still approves everything.'],
        ['Integrated (ServiceM8 / simPRO, staff-led)', '2.0 \u2013 3.0\u00d7', 'Job workflows, compliance forms and recurring contracts run on software. Owner is strategic, not operational.'],
    ], colWidths=[50*mm, 28*mm, 92*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    E.append(t)
    E.append(Spacer(1, 10))
    E.append(P('Two modifiers move you within (and sometimes beyond) these bands:'))
    E.append(B('<b>Recurring revenue.</b> More than ~25% recurring revenue (maintenance contracts, monitoring, service agreements) '
               'adds roughly +0.2\u00d7 to the multiple. Predictable income is the single most valuable thing you can add.'))
    E.append(B('<b>Owner dependence.</b> A solo operator who is also the senior tradie is high key-person risk and gets discounted '
               '(\u22120.2\u00d7). A business with a trained management layer and documented SOPs earns the premium.'))
    E.append(PageBreak())

    # ── 3. Benchmarks ──
    E.append(P('3. 2026 Benchmark Multiples by Trade', 'h1'))
    E.append(P('Benchmarks vary by trade and by how the business is structured. The figures below are indicative planning ranges '
               'observed in the Australian small-business sale market as of 2026 \u2014 not guarantees.'))
    E.append(Spacer(1, 6))
    t2 = Table([
        [Paragraph('<b>Trade</b>', styles['callout']), Paragraph('<b>SDE multiple range</b>', styles['callout']), Paragraph('<b>Notes</b>', styles['callout'])],
        ['Electrical contracting', '1.3 \u2013 2.8\u00d7', 'Higher end when CCEW/compliance is systemised and recurring contracts exist.'],
        ['Solar installation', '1.2 \u2013 2.5\u00d7', 'STC/compliance burden cuts margin; recurring monitoring lifts the multiple.'],
        ['HVAC / refrigeration', '1.4 \u2013 2.8\u00d7', 'Service contracts are common and highly valued by buyers.'],
        ['Plumbing', '1.3 \u2013 2.6\u00d7', 'Maintenance contracts and a branded reputation move the needle.'],
        ['Landscaping / outdoor', '1.1 \u2013 2.2\u00d7', 'Lower barrier to entry; recurring garden-care plans add value.'],
    ], colWidths=[42*mm, 34*mm, 94*mm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    E.append(t2)
    E.append(Spacer(1, 10))
    E.append(P('Reading the table: an electrical contracting business doing $1.2M revenue at a 15% margin has SDE of $180K. '
               'At a 1.3\u00d7 multiple that\u2019s ~$234K; at 2.8\u00d7 it\u2019s ~$504K. The \u00d71.5 spread between the two ends is '
               'entirely about systems, recurring revenue and owner dependence \u2014 not about getting more jobs.'))
    E.append(PageBreak())

    # ── 4. Seven value drivers ──
    E.append(P('4. The Seven Value Drivers', 'h1'))
    E.append(P('Buyers and valuers score businesses against a short list of drivers. Each one moves your multiple up or down.'))
    for title, desc in [
        ('1. Recurring revenue', 'The % of revenue from contracts, plans and subscriptions. The higher, the better.'),
        ('2. Owner independence', 'Can the business run for 4 weeks without you? Documented SOPs and a trained team prove it.'),
        ('3. Systems & software', 'Integrated job management (ServiceM8 / simPRO) + accounting + compliance forms. Systems are literally worth money.'),
        ('4. Compliance discipline', 'Clean CCEW/CES/STC records and audit readiness. Messy compliance = deal risk = discount.'),
        ('5. Margin quality', 'Tracked job-level profitability. Buyers pay for predictable margins, not hopeful ones.'),
        ('6. Customer concentration', 'No single client over ~20% of revenue. Diversified revenue is safer and more valuable.'),
        ('7. Growth story', 'A documented pipeline and a marketing engine that isn\u2019t just word-of-mouth.'),
    ]:
        E.append(P('<b>%s</b> \u2014 %s' % (title, desc), 'body'))
    E.append(PageBreak())

    # ── 5. Scorecard ──
    E.append(P('5. Buyer-Readiness Scorecard', 'h1'))
    E.append(P('Score yourself 1\u20135 on each. Be honest \u2014 this is for you, not a buyer.'))
    E.append(Spacer(1, 6))
    score_items = [
        'Recurring revenue is above 25% of total.',
        'The business runs for a month without the owner\u2019s daily involvement.',
        'Every job type has a documented workflow in software.',
        'Compliance certificates are generated and filed on time, every time.',
        'I know gross margin per job type (not just per year).',
        'No single client is more than 20% of revenue.',
        'There is a documented sales pipeline beyond word-of-mouth.',
    ]
    rows = [[Paragraph('<b>Statement</b>', styles['callout']), Paragraph('<b>Score (1\u20135)</b>', styles['callout'])]]
    for s in score_items:
        rows.append([Paragraph(s, styles['body']), '___'])
    t3 = Table(rows, colWidths=[156*mm, 14*mm])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    E.append(t3)
    E.append(Spacer(1, 8))
    E.append(P('<b>28\u201335:</b> exit-ready asset \u2014 you command the top of the multiple range. <b>20\u201327:</b> solid but '
               'bottlenecked \u2014 focus on the lowest scores first. <b>Under 20:</b> high key-person risk \u2014 buyers will '
               'discount heavily until systems and recurring revenue are built.', 'body'))
    E.append(PageBreak())

    # ── 6. Recurring revenue ──
    E.append(P('6. Recurring Revenue: The Biggest Single Lever', 'h1'))
    E.append(P('Nothing moves your multiple faster than predictable income. Here\u2019s why it compounds:'))
    E.append(B('<b>Buyers value certainty.</b> A dollar of contracted revenue is worth more than a dollar of \u201cwe\u2019ll probably '
               'win that job\u201d revenue. Recurring revenue de-risks the purchase.'))
    E.append(B('<b>It\u2019s systemic, not seasonal.</b> Maintenance contracts smooth the feast-and-famine cycle that scares buyers away.'))
    E.append(B('<b>It\u2019s measurable.</b> You can point to a churn rate and a book of recurring revenue \u2014 hard evidence, not a story.'))
    E.append(Spacer(1, 4))
    E.append(P('How to build it from a service business:'))
    E.append(B('Convert one-off installs into maintenance agreements, annual inspections and monitoring subscriptions.'))
    E.append(B('Automate the scheduling and renewal in your job management software so it runs without admin effort.'))
    E.append(B('Bundle compliance checks (RCD testing, STC paperwork, CCEW lodgement) into a recurring plan \u2014 it\u2019s a natural '
               'fit for electrical and solar businesses.'))
    E.append(PageBreak())

    # ── 7. 90-day plan ──
    E.append(P('7. The 90-Day Value-Building Plan', 'h1'))
    E.append(P('Three months is enough to move your multiple by a meaningful amount. Work the plan in order.'))
    E.append(Spacer(1, 4))
    for phase, items in [
        ('Days 1\u201330 \u2014 Know your numbers', [
            'Pull your SDE: net profit + owner drawings + perks. Get this number solid.',
            'Work out gross margin per job type. Stop doing the job types that lose money.',
            'List every client by revenue. Flag any single client over 20% of total.',
        ]),
        ('Days 31\u201360 \u2014 Systemise the operation', [
            'Document your 5 most common job types as workflows in your job management software.',
            'Make compliance forms mandatory \u2014 jobs can\u2019t close until certificates are done.',
            'Connect job management to accounting (Xero/MYOB) so margins are tracked live.',
        ]),
        ('Days 61\u201390 \u2014 Build recurring revenue', [
            'Launch a maintenance / service plan and convert your 10 best clients first.',
            'Automate renewals and scheduling so recurring jobs run themselves.',
            'Draft the one-page \u201cwhy this business is buyable\u201d summary a broker will need.',
        ]),
    ]:
        E.append(P('<b>%s</b>' % phase, 'h2'))
        for it in items:
            E.append(B(it))
    E.append(PageBreak())

    # ── 8. Value killers ──
    E.append(P('8. Common Value Killers', 'h1'))
    E.append(P('These are the things that make buyers walk away or lowball you. Fix them before you go to market.'))
    for k in [
        '<b>Owner is the business.</b> If everything lives in your head, there\u2019s nothing to buy. Document and delegate.',
        '<b>Messy compliance records.</b> Missing CCEW/CES/STC paperwork is a liability, not an asset. Clean it up.',
        '<b>Customer concentration.</b> One client at 40%+ of revenue is a single point of failure. Diversify.',
        '<b>Cash-flow lumpiness.</b> Feast-and-famine revenue scares buyers. Recurring contracts smooth it.',
        '<b>No margin visibility.</b> \u201cWe\u2019re doing okay\u201d isn\u2019t a number. Buyers want job-level profitability.',
        '<b>Undocumented processes.</b> If a key person leaves and the knowledge goes with them, the value drops.',
    ]:
        E.append(B(k))
    E.append(PageBreak())

    # ── 9. Documents ──
    E.append(P('9. What Buyers Will Ask For', 'h1'))
    E.append(P('When you\u2019re ready to sell, be ready to hand over:'))
    for d in [
        'Three years of financials (P&amp;L, balance sheet, BAS statements).',
        'A job-type margin breakdown.',
        'The recurring revenue book (contracts, churn rate, renewal dates).',
        'Compliance records and audit history.',
        'A staff list with roles, tenure and wages.',
        'A list of systems/software and how they\u2019re configured.',
        'The owner\u2019s transition plan (how long you\u2019ll stay on, what you\u2019ll hand over).',
    ]:
        E.append(B(d))
    E.append(Spacer(1, 8))
    E.append(P('Having these ready before a buyer asks doesn\u2019t just speed the sale \u2014 it signals a well-run business and '
               'protects your multiple during negotiation.'))
    E.append(PageBreak())

    # ── 10. Next steps ──
    E.append(P('10. Getting a Professional Read \u2014 and Next Steps', 'h1'))
    E.append(P('This report gives you the framework and the estimate. Before any transaction, get a professional opinion:'))
    E.append(B('<b>A licensed business valuer</b> for a defensible, independent number.'))
    E.append(B('<b>An M&amp;A or business broker</b> (e.g. Link Business Brokers, Benchmark, Eden Exchange) to value and list the business.'))
    E.append(B('<b>Your accountant</b> to structure the sale tax-efficiently.'))
    E.append(Spacer(1, 6))
    E.append(P('Your immediate next steps:'))
    E.append(B('Run the free calculator at tradieautomate.com/tools/business-value-calculator to get your range.'))
    E.append(B('Complete the buyer-readiness scorecard in section 5.'))
    E.append(B('Start the 90-day plan \u2014 focus on the value driver with your lowest score.'))
    E.append(Spacer(1, 10))
    E.append(HRFlowable(width='100%', thickness=1, color=BORDER))
    E.append(Spacer(1, 8))
    E.append(Paragraph('<i>Disclaimer: This report is educational and provides an estimate for planning purposes only. It is not a '
                       'professional business valuation, and it is not financial, legal or tax advice. Actual sale prices depend on the '
                       'specific buyer, market conditions and the outcome of due diligence. Consult a licensed valuer, broker and '
                       'accountant before any transaction.</i>', styles['small']))
    E.append(Spacer(1, 12))
    E.append(Paragraph('tradieautomate.com \u00b7 Australian trade business systems', styles['small']))

    doc.build(E, onFirstPage=header_footer, onLaterPages=header_footer)
    print('saved', OUT)

if __name__ == '__main__':
    build()
