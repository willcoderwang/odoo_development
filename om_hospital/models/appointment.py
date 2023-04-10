from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient", ondelete="restrict")
    gender = fields.Selection(related="patient_id.gender", readonly=False)
    appointment_time = fields.Datetime(default=fields.Datetime.now)
    booking_date = fields.Date(default=fields.Date.context_today)

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


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string="price", related="product_id.list_price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment')
