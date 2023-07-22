import random

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _order = 'id desc'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient", ondelete="restrict")
    gender = fields.Selection(related="patient_id.gender", readonly=False)
    appointment_time = fields.Datetime(default=fields.Datetime.now)
    booking_date = fields.Date(default=fields.Date.context_today)
    duration = fields.Float()

    ref = fields.Char(string="Reference", help="Reference from patient record")
    prescription = fields.Html()
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Canceled')], default="draft", string="Status", required=True)
    doctor_id = fields.Many2one('res.users')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")
    hide_sale_price = fields.Boolean()
    operation_id = fields.Many2one('hospital.operation')
    progress = fields.Integer(compute='_compute_progress', store=True)
    progress_max = fields.Integer(default=100)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can only delete appointment with draft status!"))

        return super().unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("Button Clicked !!!!!!!!!!!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Click Successful",
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            progress = 0
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100

            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string="price", related="product_id.list_price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment')
