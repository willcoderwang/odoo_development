from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    name = fields.Char(string="Name", required=True)

    def test_function(self):
        return
