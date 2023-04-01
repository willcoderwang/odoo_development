import datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if not res.get('date_cancel'):
            res['date_cancel'] = datetime.date.today()

        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', domain=[('state', '=', 'draft')])
    reason = fields.Text()
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        if self.appointment_id.booking_date <= fields.Date.today():
            raise ValidationError(_("Sorry, cancellation is not allowed on the same day or after of booking!"))
        return
