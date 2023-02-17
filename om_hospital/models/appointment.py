from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient")
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
