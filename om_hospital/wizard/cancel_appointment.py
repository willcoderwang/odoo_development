import datetime

from odoo import fields, models, api


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if not res.get('date_cancel'):
            res['date_cancel'] = datetime.date.today()
        return res

    appointment_id = fields.Many2one('hospital.appointment')
    reason = fields.Text()
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        return
