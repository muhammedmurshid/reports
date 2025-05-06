from odoo import fields,models,api,_
from datetime import date, datetime, time


class CreditNotes(models.Model):
    _name = 'op.credit.notes'
    _description = 'Credit Notes'
    _order = 'id desc'

    date = fields.Date(string="Date")
    voucher_no = fields.Char(string="Voucher No", readonly=True, copy=False)
    admission_no = fields.Char(string="Admission No.")
    fee_type = fields.Char(string="Fee Type")
    batch_id = fields.Many2one('op.batch', string="Batch")
    amount = fields.Float(string="Amount")
    student_id = fields.Many2one('op.student', string="Student")
    refund_id = fields.Many2one('student.refund', string="Refund")
    refund_given_by = fields.Many2one('res.users', string="Refund Given By")
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.user.company_id.currency_id.id)

    @api.model
    def create(self, vals):
        current_year = datetime.today().year
        # Count existing records with the same year prefix
        count = self.search_count([('voucher_no', 'ilike', f'CRN-{current_year}/')])
        serial = f"CRN-{current_year}/{str(count + 1).zfill(3)}"
        vals['voucher_no'] = serial
        return super(CreditNotes, self).create(vals)