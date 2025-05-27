from odoo import fields,models,api,_
from datetime import date

class DiscountReports(models.Model):
    _name = "discount.report"

    student_id = fields.Many2one('op.student', string="Student")
    added_date = fields.Date(string="Added Date")
    approved_date = fields.Date(string="Approved Date")
    amount = fields.Float(string="Amount")
    discount_scheme = fields.Selection([('special', 'Special'), ('scholarship', 'Scholarship')], string="Scheme",
                                       required=True)
    name = fields.Char(string="Student Name")
    sequence_no = fields.Char(string='Sequence Number', readonly=True, default='/')

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', '/') == '/':
            vals['sequence_no'] = self._generate_sequence_no()
        return super(DiscountReports, self).create(vals)

    def _generate_sequence_no(self):
        """Generate sequence number in the format DISC-YYYY-###"""
        year = date.today().year
        prefix = f"DISC-{year}"

        # Search for the latest sequence number for the current year
        last_record = self.search(
            [('sequence_no', 'like', f"{prefix}-%")],
            order="sequence_no desc",
            limit=1
        )

        if last_record:
            last_number = int(last_record.sequence_no.split("-")[-1]) + 1
        else:
            last_number = 1

        return f"{prefix}-{str(last_number).zfill(3)}"



