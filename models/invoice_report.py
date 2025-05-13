from odoo import fields,models, api, _
import re
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
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
    company_id = fields.Many2one(string='Company', comodel_name='res.company', required=True, default=lambda self: self.env.company)
    fee_name = fields.Char(string="Fee Name")
    tax = fields.Float(string="Tax")
    amount_exc_tax = fields.Float(string="Amount (Exc Tax)")
    admission_no = fields.Char(string="Admission No.", related="student_id.gr_no")
    admission_date = fields.Date(string="Admission Date", related="student_id.admission_date")
    state = fields.Selection([('completed', 'Completed'), ('cancelled','Cancelled')], string="Status", default="completed")
    is_current_month = fields.Boolean(
        string='Is Current Month',
        compute='_compute_is_current_month',
        store=True
    )

    @api.depends('date')
    def _compute_is_current_month(self):
        today = datetime.today()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month + relativedelta(months=1)
        for record in self:
            if record.date:
                record.is_current_month = (
                        record.date >= start_of_month.date() and
                        record.date < end_of_month.date()
                )
            else:
                record.is_current_month = False

    @api.depends('amount_inc_tax')
    def _compute_amount_in_words(self):
        print('workssssss')
        for i in self:
            i.amount_in_words = num2words(i.amount_inc_tax, lang='en').upper()


    amount_in_words_non_tax = fields.Char(string="Amount in Words", compute="_compute_amount_in_words_non_tax", store=1)

    @api.depends('amount_exc_tax')
    def _compute_amount_in_words_non_tax(self):
        print('workssssss')
        for i in self:
            i.amount_in_words_non_tax = num2words(i.amount_exc_tax, lang='en').upper()

    def _generate_invoice_number(self, fee_type):
        """Generate a unique Invoice Number with separate sequences for Normal and Ancillary Fees."""

        today = date.today()
        year = today.year
        month = today.month

        # Determine academic year (April to March)
        if month >= 4:  # If April or later, use current year as start
            academic_year = f"{year}-{str(year + 1)[-2:]}"
        else:  # If Jan-March, use previous year as start
            academic_year = f"{year - 1}-{str(year)[-2:]}"

        # Define prefix based on fee type
        if fee_type == "Collection A/C":
            print('yaaaaaaaaa', fee_type)
            prefix = f"VXL-ANC-{academic_year}/"
        else:
            print('noo', fee_type)
            prefix = f"VXL-{academic_year}/"

        # Get all invoice numbers for the current academic year of the same type
        existing_invoices = self.search([('invoice_number', 'like', prefix + '%')])

        highest_number = 0
        for invoice in existing_invoices:
            match = re.search(r"/(\d+)$", invoice.invoice_number)
            if match:
                number = int(match.group(1))
                highest_number = max(highest_number, number)

        new_number = highest_number + 1  # Get next number in sequence

        return f"{prefix}{new_number:02d}"

    def create(self, vals):
        """Override create method to generate invoice number"""
        if 'fee_type' in vals:
            vals['invoice_number'] = self._generate_invoice_number(vals['fee_type'])  # Pass fee_type
        else:
            raise ValueError("Missing required field 'fee_type' for invoice generation")
        return super(InvoiceReports, self).create(vals)

    def act_print_invoice(self):
        print('k')
        return self.env.ref('reports.action_report_students_payment_history_receipt').report_action(self)

    def act_print_invoice_non_tax(self):
        print('k')
        return self.env.ref('reports.action_report_students_payment_history_receipt_non_tax').report_action(self)

