from odoo import fields, models


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = "Patient Tag"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer()
    color_2 = fields.Char()
