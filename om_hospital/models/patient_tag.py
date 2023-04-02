from odoo import fields, models, api


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = "Patient Tag"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(copy=False)
    color_2 = fields.Char()
    sequence = fields.Integer()

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
        ('check_sequence', 'check(sequence > 0)', 'The sequence must be a non zero positive number!')
    ]

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get('name'):
            default['name'] = f"{self.name} (copy)"

        default['sequence'] = 10
        return super().copy(default)
