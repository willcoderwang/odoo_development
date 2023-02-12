from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient")
    gender = fields.Selection(related="patient_id.gender", readonly=False)
    appointment_time = fields.Datetime(default=fields.Datetime.now)
    booking_date = fields.Date(default=fields.Date.context_today)

    ref = fields.Char(string="Reference")

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref
