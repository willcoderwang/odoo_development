from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', string="Confirmed User")

    def action_confirm(self):
        super().action_confirm()
        self.confirmed_user_id = self.env.user.id
