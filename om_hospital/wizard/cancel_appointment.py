import datetime

from dateutil.relativedelta import relativedelta

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
        cancel_days = int(self.env['ir.config_parameter'].sudo().get_param('om_hospital.cancel_days'))

        if self.appointment_id.booking_date - relativedelta(days=cancel_days) <= fields.Date.today():
            raise ValidationError(_("Sorry, cancellation is not allowed on the same day or after of booking!"))
        self.appointment_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
