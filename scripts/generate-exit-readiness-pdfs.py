#!/usr/bin/env python3
"""Generate 3-tier Exit-Readiness Action Plan PDFs using Arial font."""

from fpdf import FPDF

FONT_PATH = '/System/Library/Fonts/Supplemental/Arial.ttf'
FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
OUTPUT_DIR = '/Users/shane/tradieautomate/repo/public'

# ServiceM8 affiliate URL
SM8_URL = 'https://www.servicem8.com/?ref=tradieautomate&utm_source=tradieautomate&utm_medium=pdf&utm_campaign=exit-readiness-quiz'


class ExitReadinessPDF(FPDF):
    def __init__(self, tier):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.add_font('Arial', '', FONT_PATH, uni=True)
        self.add_font('Arial', 'B', FONT_BOLD, uni=True)
        self.set_auto_page_break(auto=True, margin=20)
        self.tier = tier

    def header(self):
        if self.page_no() > 1:
            return
        # Top orange bar
        self.set_fill_color(249, 115, 22)
        self.rect(0, 0, 210, 5, 'F')
        self.ln(8)

    def footer(self):
        self.set_y(-16)
        self.set_font('Arial', '', 7)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, 'TradieAutomate.com — Exit-Readiness Action Plan — Page ' + str(self.page_no()), align='C')

    def navy_header(self, text):
        self.set_fill_color(15, 23, 42)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, f'  {text}', fill=True)
        self.ln(10)

    def orange_sub(self, text):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(249, 115, 22)
        self.cell(0, 6, text)
        self.ln(6)

    def body_text(self, text):
        self.set_font('Arial', '', 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def action_item(self, num, title, detail):
        # Number circle
        self.set_fill_color(15, 23, 42)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 9)
        x = self.get_x()
        y = self.get_y()
        self.cell(8, 8, str(num), fill=True, align='C')
        # Title
        self.set_xy(x + 10, y)
        self.set_text_color(15, 23, 42)
        self.set_font('Arial', 'B', 9)
        self.cell(0, 4, title)
        self.ln(4.5)
        # Detail
        self.set_x(x + 10)
        self.set_text_color(71, 85, 105)
        self.set_font('Arial', '', 8)
        self.multi_cell(0, 4, detail)
        self.ln(3)

    def cta_box(self):
        self.ln(4)
        self.set_draw_color(249, 115, 22)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(15, y, 195, y)
        self.ln(5)
        self.set_fill_color(255, 248, 240)
        self.set_draw_color(249, 115, 22)
        self.rect(15, self.get_y(), 180, 42, 'DF')
        self.set_xy(20, self.get_y() + 4)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(15, 23, 42)
        self.cell(170, 5, 'Ready to systemise your business?', align='C')
        self.ln(7)
        self.set_x(20)
        self.set_font('Arial', 'B', 9)
        self.set_text_color(249, 115, 22)
        self.cell(170, 5, 'Start your free ServiceM8 trial', align='C', link=SM8_URL)
        self.ln(6)
        self.set_x(20)
        self.set_font('Arial', '', 7)
        self.set_text_color(100, 116, 139)
        self.cell(170, 5, SM8_URL, align='C')
        self.ln(5)
        self.set_x(20)
        self.set_font('Arial', '', 7)
        self.set_text_color(100, 116, 139)
        self.cell(170, 5, '14-day free trial. No credit card. Unlimited staff. CCEW compliance forms built in.', align='C')
        self.ln(14)

    def related_reading(self, articles):
        self.ln(2)
        self.orange_sub('Continue Reading on TradieAutomate')
        self.set_font('Arial', '', 8)
        self.set_text_color(51, 65, 85)
        for title, url in articles:
            self.set_text_color(249, 115, 22)
            self.cell(4, 5, '•')
            self.set_text_color(51, 65, 85)
            self.cell(0, 5, f'  {title}', link=f'https://tradieautomate.com{url}')
            self.ln(4.5)
        self.ln(2)


def build_high_risk():
    pdf = ExitReadinessPDF('high-risk')
    pdf.add_page()

    # Hero section
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, 'Exit-Readiness Action Plan', align='C')
    pdf.ln(6)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(239, 68, 68)
    pdf.cell(0, 6, 'High Key-Person Risk — Your Business Is a Job, Not an Asset', align='C')
    pdf.ln(10)

    # Score summary
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, 'Based on your quiz responses, your business depends almost entirely on you. Buyers see this and discount heavily —', align='C')
    pdf.ln(4)
    pdf.cell(0, 5, 'or walk away entirely. The good news: every problem the quiz identified has a fix.', align='C')
    pdf.ln(10)

    # Diagnosis
    pdf.navy_header('Your Diagnosis')
    pdf.body_text(
        'Your business is currently a job, not a sellable asset. It relies on your time, energy, and personal memory. '
        'Quoting happens in your head, compliance paperwork lives in WhatsApp, and if you took a month off, the business '
        'would stall. Buyers buy systems, not people — and right now, the system IS you.'
    )
    pdf.body_text(
        'The fix starts with three things: get off the tools, centralise your pricing, and build job workflows that '
        'don\'t depend on you being there. Every one of these is achievable in 3-6 months with the right software.'
    )

    # Top 3 actions
    pdf.navy_header('Your Top 3 Priority Actions')
    pdf.action_item('1', 'Centralise your quoting rules and pricing',
        'Stop building quotes from memory. Set up standardised pricing templates with pre-loaded supplier costs, '
        'labour rates, and margin targets. When every quote follows the same rules, you stop being the bottleneck — '
        'and you stop leaving money on the table. ServiceM8\'s quoting engine handles this out of the box.')
    pdf.action_item('2', 'Build systemised SOPs in job management software',
        'Every job type needs a documented workflow: what happens at booking, what forms are required on site, '
        'what photos must be captured, what sign-off steps close the job. Build these once in ServiceM8, and every '
        'technician — including ones you haven\'t hired yet — follows the same process.')
    pdf.action_item('3', 'Start tracking job profitability per job type',
        'You can\'t fix margins you can\'t see. Connect your job management to Xero or MYOB so labour hours and '
        'supplier costs are tracked against every job in real time. Within 3 months, you\'ll know exactly which '
        'job types make money and which are quietly bleeding it.')

    # Related reading
    pdf.related_reading([
        ('ServiceM8 for Electricians — Full Guide', '/blog/servicem8-for-electricians'),
        ('How to Sell Your ServiceM8-Based Trade Business', '/blog/sell-servicem8-trade-business-value'),
        ('Hidden Costs Killing Your Profit as a Solar Installer or Electrician', '/blog/hidden-costs-killing-profit-solar-electrician'),
    ])

    # CTA
    pdf.cta_box()

    # Playbook mention
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, 'This action plan is a starting point. For the complete system — 12 chapters covering licensing, cash flow,', align='C')
    pdf.ln(4)
    pdf.cell(0, 5, 'tech stack, hiring, and building a business worth selling — download The Sparky\'s Playbook (free):', align='C')
    pdf.ln(4)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(249, 115, 22)
    pdf.cell(0, 5, 'tradieautomate.com/playbook', align='C', link='https://tradieautomate.com/playbook')

    path = f'{OUTPUT_DIR}/exit-readiness-plan-high-risk.pdf'
    pdf.output(path)
    print(f'✅ {path} — {pdf.pages_count} page(s)')


def build_scaling_trap():
    pdf = ExitReadinessPDF('scaling-trap')
    pdf.add_page()

    # Hero
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, 'Exit-Readiness Action Plan', align='C')
    pdf.ln(6)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(217, 165, 0)
    pdf.cell(0, 6, 'The Scaling Trap — You\'ve Grown, But You\'re Still the Bottleneck', align='C')
    pdf.ln(10)

    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, 'You\'ve built a real business — but you\'re still the pin in every process. Buyers see potential here,', align='C')
    pdf.ln(4)
    pdf.cell(0, 5, 'but they\'ll discount for the key-person risk. Fix the bottlenecks and your multiple jumps.', align='C')
    pdf.ln(10)

    # Diagnosis
    pdf.navy_header('Your Diagnosis')
    pdf.body_text(
        'You\'ve grown beyond a solo operation, but you\'re the operational bottleneck. You have basic systems in place '
        '— maybe Xero for accounting, some checklists for the crew — but you lack the automation to remove yourself '
        'from day-to-day admin, compliance chasing, and job costing.'
    )
    pdf.body_text(
        'The scaling trap is common: the business grew faster than the systems. The fix isn\'t working harder — '
        'it\'s connecting the tools you already have so they talk to each other without you in the middle.'
    )

    # Top 3 actions
    pdf.navy_header('Your Top 3 Priority Actions')
    pdf.action_item('1', 'Automate compliance documentation so jobs close without you',
        'Right now you\'re chasing technicians for missing photos, blurry serial numbers, and unsigned CCEW forms. '
        'ServiceM8\'s digital job forms make compliance mandatory — jobs can\'t be marked complete until all checks '
        'pass automated validation. The Friday afternoon paperwork scramble disappears.')
    pdf.action_item('2', 'Build recurring revenue streams',
        'Zero recurring revenue is the single biggest drag on your valuation multiple. Start converting one-off clients '
        'into maintenance contracts, annual inspection agreements, and monitoring subscriptions. Even 10-15% recurring '
        'revenue can add 0.5-1x to your EBIT multiple. ServiceM8\'s scheduling engine handles recurring job creation automatically.')
    pdf.action_item('3', 'Integrate your tech stack end-to-end',
        'You have the pieces — accounting software, maybe some scheduling tools — but they don\'t talk to each other. '
        'Connect ServiceM8 to Xero or MYOB so invoices, payments, and client records sync automatically. One source '
        'of truth. No double-entry. Live job profitability at your fingertips.')

    # Related reading
    pdf.related_reading([
        ('Full ServiceM8 Review 2026 — Pricing, Features & Who It Suits', '/blog/servicem8-review-2026'),
        ('How to Sell Your ServiceM8-Based Trade Business', '/blog/sell-servicem8-trade-business-value'),
        ('Solar Monitoring & After-Sales Revenue Guide', '/blog/solar-monitoring-after-sales-revenue-australia'),
    ])

    # CTA
    pdf.cta_box()

    # Playbook
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, 'This action plan is a starting point. For the complete system — 12 chapters covering licensing, cash flow,', align='C')
    pdf.ln(4)
    pdf.cell(0, 5, 'tech stack, hiring, and building a business worth selling — download The Sparky\'s Playbook (free):', align='C')
    pdf.ln(4)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(249, 115, 22)
    pdf.cell(0, 5, 'tradieautomate.com/playbook', align='C', link='https://tradieautomate.com/playbook')

    path = f'{OUTPUT_DIR}/exit-readiness-plan-scaling-trap.pdf'
    pdf.output(path)
    print(f'✅ {path} — {pdf.pages_count} page(s)')


def build_exit_ready():
    pdf = ExitReadinessPDF('exit-ready')
    pdf.add_page()

    # Hero
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, 'Exit-Readiness Action Plan', align='C')
    pdf.ln(6)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 6, 'Exit-Ready Asset — Your Business Is Built to Sell', align='C')
    pdf.ln(10)

    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, 'Your business has the systems, documentation, and management layer buyers pay a premium for.', align='C')
    pdf.ln(4)
    pdf.cell(0, 5, 'Now it\'s about maximising that multiple and preparing the transition.', align='C')
    pdf.ln(10)

    # Diagnosis
    pdf.navy_header('Your Diagnosis')
    pdf.body_text(
        'You\'ve successfully decoupled your time from business revenue. Low key-person risk, automated compliance, '
        'real-time margin visibility, and a management layer that runs without you — this is exactly what buyers want '
        'to see. Your business is an attractive, high-multiple acquisition target.'
    )
    pdf.body_text(
        'At this stage, the work shifts from building systems to optimising for exit: maximising recurring revenue, '
        'getting a professional valuation, and preparing the leadership transition plan that lets you walk away clean.'
    )

    # Top 3 actions
    pdf.navy_header('Your Top 3 Priority Actions')
    pdf.action_item('1', 'Maximise recurring revenue to boost your EBIT multiple',
        'Every percentage point of recurring revenue — maintenance contracts, monitoring subscriptions, service '
        'agreements — adds measurable value to your exit multiple. A business with 20%+ recurring revenue can command '
        '3-4x EBIT vs 2-2.5x for comparable project-only businesses. ServiceM8\'s scheduling engine makes recurring '
        'job management automatic.')
    pdf.action_item('2', 'Get a professional valuation to benchmark your exit number',
        'Engage a business broker with specific trade business experience. They\'ll assess your ServiceM8 records, '
        'financials, customer concentration, and growth trajectory to establish a defensible valuation. Knowing your '
        'number lets you negotiate from strength and identify gaps before a buyer does.')
    pdf.action_item('3', 'Prepare your 3-year transition plan for leadership and key accounts',
        'Even an exit-ready business needs a handover. Document the transition timeline: when key accounts get '
        'introduced to new management, when supplier relationships transfer, when you step back from daily operations. '
        'A clean 12-36 month transition plan is the difference between a good exit and a great one.')

    # Related reading
    pdf.related_reading([
        ('How to Sell Your ServiceM8-Based Trade Business for Maximum Value', '/blog/sell-servicem8-trade-business-value'),
        ('The Modern Trade Tech Stack — Chapter 8 of The Sparky\'s Playbook', '/blog/sparkys-playbook-chapter-8-trade-tech-stack-job-management-accounting'),
        ('Scaling Your Electrical Business — Chapter 11', '/blog/sparkys-playbook-chapter-11-scaling-electrical-business-australia'),
    ])

    # CTA
    pdf.cta_box()

    # Playbook
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, 'Ready to benchmark your exit? Download The Sparky\'s Playbook — the free 12-chapter guide covering', align='C')
    pdf.ln(4)
    pdf.cell(0, 5, 'everything from licensing to cash flow to building a business worth selling:', align='C')
    pdf.ln(4)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(249, 115, 22)
    pdf.cell(0, 5, 'tradieautomate.com/playbook', align='C', link='https://tradieautomate.com/playbook')

    path = f'{OUTPUT_DIR}/exit-readiness-plan-exit-ready.pdf'
    pdf.output(path)
    print(f'✅ {path} — {pdf.pages_count} page(s)')


if __name__ == '__main__':
    build_high_risk()
    build_scaling_trap()
    build_exit_ready()
    print('\nAll 3 action plan PDFs generated.')
    print(f'Output directory: {OUTPUT_DIR}/')
    print(f'\nVerify:')
    print(f'  https://tradieautomate.com/exit-readiness-plan-high-risk.pdf')
    print(f'  https://tradieautomate.com/exit-readiness-plan-scaling-trap.pdf')
    print(f'  https://tradieautomate.com/exit-readiness-plan-exit-ready.pdf')