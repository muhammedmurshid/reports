from odoo import fields,models,api, _

class InheritLeads(models.Model):
    _inherit = 'leads.logic'

    report = fields.Many2one('invoice.reports', string="Invoice")
