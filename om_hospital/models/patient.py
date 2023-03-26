from datetime import date

from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patient"

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date()
    ref = fields.Char(string="Reference", default=lambda self: self.env['ir.sequence'].next_by_code('hospital.patient'))
    age = fields.Integer(string="Age", compute="_compute_age", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender", tracking=True, default='female')
    active = fields.Boolean(default=True)
    image = fields.Image()
    tag_ids = fields.Many2many('patient.tag')

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year - (
                        (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            else:
                rec.age = 0
