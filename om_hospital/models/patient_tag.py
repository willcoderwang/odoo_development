from odoo import fields, models


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = "Patient Tag"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer()
    color_2 = fields.Char()
    sequence = fields.Integer()

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
        ('check_sequence', 'check(sequence > 0)', 'The sequence must be a non zero positive number!')
    ]
