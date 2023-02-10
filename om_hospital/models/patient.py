from odoo import models, fields


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patient"

    name = fields.Char(string="Name", tracking=True)
    ref = fields.Char(string="Reference", default="Odoo Mates")
    age = fields.Integer(string="Age", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender", tracking=True, default='female')
    active = fields.Boolean(default=True)
