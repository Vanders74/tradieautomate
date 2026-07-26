#!/usr/bin/env python3
"""Generate the Electrical Award Rates Quick Reference Card PDF using Arial Unicode font."""

from fpdf import FPDF

FONT_PATH = '/System/Library/Fonts/Supplemental/Arial.ttf'
FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'


class AwardRatesPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.add_font('Arial', '', FONT_PATH, uni=True)
        self.add_font('Arial', 'B', FONT_BOLD, uni=True)
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() == 1:
            return  # Header handled explicitly on page 1
        self.set_font('Arial', 'B', 9)
        self.set_text_color(26, 39, 68)
        self.cell(0, 5, 'MA000025 Electrical Award Rates -- Quick Reference Card', align='C')
        self.ln(1)
        self.set_draw_color(249, 115, 22)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 6)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, 'Award: MA000025 | Source: Fair Work Commission AWR 2025-26 | TradieAutomate.com | Page ' + str(self.page_no()), align='C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 9)
        self.set_text_color(26, 39, 68)
        self.set_fill_color(240, 244, 255)
        self.cell(0, 6, f'  {title}', fill=True)
        self.ln(8)

    def table_header(self, cols, widths):
        self.set_font('Arial', 'B', 7)
        self.set_fill_color(26, 39, 68)
        self.set_text_color(255, 255, 255)
        for col, w in zip(cols, widths):
            self.cell(w, 5.5, col, border=1, fill=True, align='C')
        self.ln()

    def table_row(self, cells, widths, alignments=None):
        self.set_font('Arial', '', 7)
        self.set_text_color(30, 41, 59)
        if alignments is None:
            alignments = ['C'] * len(cells)
        for cell, w, a in zip(cells, widths, alignments):
            self.cell(w, 5, str(cell), border=1, align=a)
        self.ln()

    def warning_note(self, num, text):
        self.set_font('Arial', 'B', 7)
        self.set_text_color(249, 115, 22)
        self.cell(7, 4, num)
        self.set_font('Arial', '', 7)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 4, text)
        self.ln(0.5)


def build_pdf():
    pdf = AwardRatesPDF()
    pdf.add_page()

    # --- PAGE 1 HEADER ---
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(26, 39, 68)
    pdf.cell(0, 8, 'MA000025 Electrical Award Rates', align='C')
    pdf.ln(6)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(249, 115, 22)
    pdf.cell(0, 6, 'Quick Reference Card -- July 2026', align='C')
    pdf.ln(3)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, 'Rates effective from first full pay period on or after 1 July 2026 | Verify at fairwork.gov.au', align='C')
    pdf.ln(2)
    pdf.set_draw_color(249, 115, 22)
    pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)

    # --- ET GRADES ---
    col_w = [52, 28, 28, 28, 34]
    pdf.section_title('Electrical Tradesperson (ET) Grades -- Hourly Rates')
    pdf.table_header(['Classification', 'Hourly', '1.5x OT', '2.0x OT', 'Weekly (38h)'], col_w)
    for g in [
        ('ET Grade 1', '$38.43', '$57.65', '$76.86', '$1,460.34'),
        ('ET Grade 2', '$39.36', '$59.04', '$78.72', '$1,495.68'),
        ('ET Grade 3', '$40.26', '$60.39', '$80.52', '$1,529.88'),
        ('ET Grade 4', '$41.20', '$61.80', '$82.40', '$1,565.60'),
        ('ET Grade 5', '$42.15', '$63.23', '$84.30', '$1,601.70'),
    ]:
        pdf.table_row(g, col_w)
    pdf.ln(5)

    # --- APPRENTICES ---
    app_w = [20, 24, 24, 24, 24, 34]
    pdf.section_title('Apprentices -- % of ET Grade 1 ($38.43/hr)')
    pdf.table_header(['Year', '% G1', 'Hourly', '1.5x OT', '2.0x OT', 'Weekly (38h)'], app_w)
    for a in [
        ('Year 1', '42%', '$16.14', '$24.21', '$32.28', '$613.32'),
        ('Year 2', '55%', '$21.14', '$31.71', '$42.28', '$803.32'),
        ('Year 3', '75%', '$28.82', '$43.23', '$57.64', '$1,095.16'),
        ('Year 4', '88%', '$33.82', '$50.73', '$67.64', '$1,285.16'),
    ]:
        pdf.table_row(a, app_w)
    pdf.ln(5)

    # --- ALLOWANCES ---
    al_w = [52, 34, 74]
    pdf.section_title('Allowances (per week unless stated)')
    pdf.table_header(['Allowance', 'Rate', 'When Applies'], al_w)
    for a in [
        ('Tool allowance', '$21.17/wk', 'Employee supplies own tools'),
        ('Industry allowance', '$47.61/wk', 'All on-site electrical installation/maintenance work'),
        ('Living away from home', '$139.30/day', 'Employee required to sleep away (check cl. 19.3)'),
        ('Meal allowance', '$17.63/meal', 'OT > 1.5 hrs, or shift extending past 7:30pm'),
        ('Vehicle allowance', '$0.99/km', 'Personal vehicle used for work travel'),
    ]:
        pdf.table_row(a, al_w, alignments=['L', 'C', 'L'])
    pdf.ln(5)

    # --- SUPER ---
    pdf.section_title('Superannuation')
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 5, 'SG Rate: 11.5% (from 1 Jul 2025)    |    Next: 12.0% from 1 July 2026    |    Calculated on Ordinary Time Earnings', align='C')
    pdf.ln(7)

    # --- OVERTIME ---
    ot_w = [90, 70]
    pdf.section_title('Overtime Rules at a Glance')
    pdf.table_header(['When', 'Rate'], ot_w)
    for o in [
        ('First 3 hours on any day', '1.5x'),
        ('After 3 hours on any day', '2.0x'),
        ('All work on Sunday', '2.0x'),
        ('All work on Public Holiday', '2.5x'),
        ('Minimum call-out (after hours)', '3 hours at double time'),
    ]:
        pdf.table_row(o, ot_w, alignments=['L', 'C'])
    pdf.ln(7)

    # --- WARNINGS ---
    pdf.section_title('Top 5 Misclassification Risks (FWO Audit Targets)')
    pdf.warning_note('1.', 'Classification matters. An electrician doing complex or supervisory work is likely Grade 3-5, not Grade 1. Misclassification is the #1 underpayment trigger in Fair Work Ombudsman audits of trade businesses.')
    pdf.warning_note('2.', 'Apprentice percentages are applied to Grade 1 rate -- not the grade of the supervising tradesperson. Common error: applying Year 3 apprentice % to Grade 3 supervisor rate.')
    pdf.warning_note('3.', 'Tool allowance applies even when tools are only partly supplied by the employee. If they bring any tools at all, the allowance applies -- check the award clause.')
    pdf.warning_note('4.', 'Industry allowance is NOT optional. It applies to all employees performing on-site electrical installation work, regardless of business size or project value.')
    pdf.warning_note('5.', 'Backpay exposure is 6 years under the Fair Work Act. A $2/hr underpayment sustained over 6 years = approximately $25,000 per employee before penalties and interest.')

    # --- CTA ---
    pdf.ln(4)
    pdf.set_draw_color(249, 115, 22)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(26, 39, 68)
    pdf.cell(0, 5, 'Full guide + interactive pay calculator:', align='C')
    pdf.ln(4)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(249, 115, 22)
    pdf.cell(0, 5, 'tradieautomate.com/blog/electrical-contractor-award-rates-australia-2026', align='C')

    # Save
    output_path = '/Users/shane/tradieautomate/repo/public/electrical-award-rates-card-2026.pdf'
    pdf.output(output_path)
    print(f'PDF saved to {output_path}')
    print(f'Pages: {pdf.pages_count}')


if __name__ == '__main__':
    build_pdf()
