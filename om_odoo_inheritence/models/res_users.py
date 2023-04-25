# -*- coding: utf-8 -*-

from odoo import api, models


class GroupsView(models.Model):
    _inherit = 'res.groups'

    @api.model
    def get_application_groups(self, domain):
        use_wave_pickings = self.env.ref('stock.group_stock_picking_wave')
        domain += [('id', 'not in', (use_wave_pickings.id,))]

        return super().get_application_groups(domain)
