from odoo import fields, models, api, _
from num2words import num2words
from datetime import date
import re

class Receipts(models.Model):
    _name = 'receipts.report'
    _order = 'id desc'

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    phone = fields.Char(string="Phone", widget='phone')
    student_id = fields.Many2one('op.student', string="Student")
    payment_mode = fields.Selection([('Cash', 'Cash'), ('Bank Direct', 'Bank Direct'), ('Gateway', 'Gateway')], string="Payment Mode")
    amount = fields.Float(string="Amount")
    branch = fields.Selection(
        [('Corporate Office & City Campus', 'Corporate Office & City Campus'), ('Cochin Campus', 'Cochin Campus'),
         ('Calicut Campus', 'Calicut Campus'), ('Trivandrum Campus', 'Trivandrum Campus'),
         ('Kottayam Campus', 'Kottayam Campus'),
         ('Perinthalmanna Branch', 'Perinthalmanna Branch'), ('Bangalore Campus', 'Bangalore Campus')], string="Branch")
    receipt_no = fields.Char("Receipt No", readonly=True, copy=False, default="/")
    company_id = fields.Many2one(string='Company', comodel_name='res.company', required=True, default=lambda self: self.env.company)
    batch = fields.Char(string="Batch")
    reference_no = fields.Char(string="Reference No.")


    @api.model
    def create(self, vals):
        if vals.get('receipt_no', '/') == '/':
            payment_mode = vals.get('payment_mode')
            vals['receipt_no'] = self._generate_receipt_no(payment_mode)
        return super(Receipts, self).create(vals)

    def _generate_receipt_no(self, payment_mode):
        """ Generate receipt number based on payment mode """
        today = date.today()
        year = today.year
        month = today.month

        # Determine financial year
        if month >= 4:  # April to December
            fy_start = year
            fy_end = year + 1
        else:  # January to March
            fy_start = year - 1
            fy_end = year

        fy_code = f"{fy_start}-{str(fy_end)[-2:]}"  # e.g., 2025-26

        # Define prefixes
        prefixes = {
            'Cash': 'VXL',
            'Bank Direct': 'VXLBD',
            'Gateway': 'VXLBG'
        }
        prefix = prefixes.get(payment_mode, 'VXLC')  # fallback

        # Determine search pattern and receipt format
        if payment_mode == 'Cash':
            search_pattern = f"{prefix}-{fy_code}/CR-%"
        else:
            search_pattern = f"{prefix}-{fy_code}/%"

        # Search for last receipt
        last_receipt = self.search(
            [('receipt_no', 'like', search_pattern)],
            order="receipt_no desc",
            limit=1
        )

        if last_receipt:
            number_part = last_receipt.receipt_no.split("/")[-1]
            if payment_mode == 'Cash':
                number_part = number_part.replace("CR-", "")
            last_number = int(number_part) + 1
        else:
            last_number = 1

        # Format final receipt number
        if payment_mode == 'Cash':
            return f"{prefix}-{fy_code}/CR-{str(last_number).zfill(3)}"
        else:
            return f"{prefix}-{fy_code}/{str(last_number).zfill(3)}"

    def act_print_receipt(self):
        print('k')
        return self.env.ref('reports.action_report_receipt').report_action(self)

    amount_in_words = fields.Char(string="Amount in Words", compute="_compute_amount_in_words", store=1)

    @api.depends('amount')
    def _compute_amount_in_words(self):
        print('workssssss')
        for i in self:
            i.amount_in_words = num2words(i.amount, lang='en').upper()

