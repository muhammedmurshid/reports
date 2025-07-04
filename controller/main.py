from odoo import http
from odoo.http import request

class InvoiceReports(http.Controller):

    @http.route('/invoice_reports/summary', type='json', auth='user')
    def get_totals(self):
        records = request.env['invoice.reports'].search([])
        return {
            'total_taxable': sum(r.taxable_amount for r in records),
            'total_cgst': sum(r.cgst for r in records),
            'total_sgst': sum(r.sgst for r in records),
            'total_amount': sum(r.total_amount for r in records),
        }

