from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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
    appointment_count = fields.Integer(compute="_compute_appointment_count", string="Appointment Count", store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status",
                                      default='single', tracking=True)
    partner_name = fields.Char(string="Partner Name")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date of birth is not acceptable."))

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You cannot delete a patient with appointments."))

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    def write(self, vals):
        return super().write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year - (
                        (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            else:
                rec.age = 0

    def name_get(self):
        return [(rec.id, f"{rec.ref} - {rec.name}") for rec in self]

    def action_test(self):
        print("Clicked...")
        return
