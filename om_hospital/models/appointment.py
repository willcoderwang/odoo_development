from odoo import models, fields


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient")
    appointment_time = fields.Datetime()
    booking_date = fields.Date()
