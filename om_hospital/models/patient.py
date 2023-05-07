from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patient"

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date()
    ref = fields.Char(string="Reference", default=lambda self: self.env['ir.sequence'].next_by_code('hospital.patient'))
    age = fields.Integer(string="Age", compute="_compute_age", inverse='_inverse_age', search='_search_age',
                         tracking=True)
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
    is_birthday = fields.Boolean(string="Birthday ?", compute="_compute_is_birthday")
    phone = fields.Char()
    email = fields.Char()
    website = fields.Char()

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        today = date.today()
        for rec in self:
            is_birthday = False
            if rec.date_of_birth and rec.date_of_birth.day == today.day and rec.date_of_birth.month == today.month:
                is_birthday = True
            rec.is_birthday = is_birthday

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

    @api.depends('age')
    def _inverse_age(self):
        for rec in self:
            rec.date_of_birth = fields.Date.today() - relativedelta(years=rec.age)

    @api.model
    def _search_age(self, operator, operand):
        date_of_birth = date.today() - relativedelta(years=operand)
        start_of_year = date_of_birth.replace(month=1, day=1)
        end_of_year = date_of_birth.replace(month=12, day=31)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    def name_get(self):
        return [(rec.id, f"{rec.ref} - {rec.name}") for rec in self]

    def action_test(self):
        print("Clicked...")
        return
