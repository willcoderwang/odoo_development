from odoo import models, fields


class PartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = ['res.partner.category', 'mail.thread']

    name = fields.Char(tracking=True)
