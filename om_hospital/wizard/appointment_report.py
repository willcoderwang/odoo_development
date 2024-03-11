from odoo import models, fields


class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = "Appointment Report Wizard"

    patient_id = fields.Many2one('hospital.patient')
    date_from = fields.Date()
    date_to = fields.Date()

    def action_print_report(self):
        domain = []
        if self.patient_id:
            domain += [('patient_id', '=', self.patient_id.id)]
        if self.date_from:
            domain += [('booking_date', '>=', self.date_from)]
        if self.date_to:
            domain += [('booking_date', '<=', self.date_to)]

        appointments = self.env['hospital.appointment'].search(domain)
        appointment_values = [{
            'name': appointment.name,
            'doctor': appointment.doctor_id.display_name,
            'duration': appointment.duration,
        } for appointment in appointments]

        data = {
            'form': self.read()[0],
            'appointments': appointment_values,
        }

        return self.env.ref('om_hospital.report_appointment').report_action(self, data=data)

    def action_print_excel_report(self):
        return self.env.ref('om_hospital.report_patient_appointment_xlsx').report_action(self, data={})
