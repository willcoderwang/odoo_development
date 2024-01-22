# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    confirmed_user_id = fields.Many2one('res.users', string="Confirmed User", readonly=True)

    def _select_additional_fields(self, fields):
        fields['confirmed_user_id'] = ", s.confirmed_user_id"
        return super()._select_additional_fields(fields)
