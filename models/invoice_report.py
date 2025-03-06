from odoo import fields,models, api, _
from datetime import date
import re
from num2words import num2words


class InvoiceReports(models.Model):
    _name = 'invoice.reports'
    _order = 'id desc'

    name = fields.Char(string="Name")
    invoice_number = fields.Char(string="Invoice Number", readonly=True, copy=False)
    branch = fields.Char(string="Branch")
    date = fields.Date(string="Date")
    fee_type = fields.Char(string="Fee Type")
    reference_no = fields.Char(string="Reference No")
    amount_inc_tax = fields.Float(string="Amount (Inc Tax)")
    fee_collected_by = fields.Many2one('res.users', string="Fee Collected By")
    lead_id = fields.Many2one('leads.logic', string="Lead")
    payment_mode = fields.Char(string="Payment Mode")
    cheque_no = fields.Char(string="Cheque No.")
    batch = fields.Char(string="Batch")
    course = fields.Char(string="course")
    student_id = fields.Many2one('op.student',string="Student")
    cgst_amount = fields.Float(string="Cgst")
    sgst_amount = fields.Float(string="Sgst")
    amount_in_words = fields.Char(string="Amount in Words", compute="_compute_amount_in_words", store=1)

    @api.depends('amount_inc_tax')
    def _compute_amount_in_words(self):
        print('workssssss')
        for i in self:
            i.amount_in_words = num2words(i.amount_inc_tax, lang='en').upper()

    def _generate_invoice_number(self):
        """Generate a unique Invoice Number with increasing count per academic year"""

        today = date.today()
        year = today.year
        month = today.month

        # Determine academic year (April to March)
        if month >= 4:  # If April or later, use current year as start
            academic_year = f"{year}-{str(year + 1)[-2:]}"
        else:  # If Jan-March, use previous year as start
            academic_year = f"{year - 1}-{str(year)[-2:]}"

        prefix = f"VXL-{academic_year}/"

        # Get all invoice numbers for the current academic year
        existing_invoices = self.search([('invoice_number', 'like', prefix + '%')])

        highest_number = 0
        for invoice in existing_invoices:
            match = re.search(r"/(\d+)$", invoice.invoice_number)
            if match:
                number = int(match.group(1))
                highest_number = max(highest_number, number)

        new_number = highest_number + 1  # Get next number

        return f"{prefix}{new_number:02d}"

    @api.model
    def create(self, vals):
        if not vals.get('invoice_number'):
            vals['invoice_number'] = self._generate_invoice_number()
        return super(InvoiceReports, self).create(vals)

    def act_print_invoice(self):
        print('k')
        return self.env.ref('reports.action_report_students_payment_history_receipt').report_action(self)

