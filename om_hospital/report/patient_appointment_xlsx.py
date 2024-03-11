from odoo import models


class PatientAppointmentXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_appointment_xlsx_template'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizards):
        wizard = wizards[0]
        domain = []
        if wizard.patient_id:
            domain += [('patient_id', '=', wizard.patient_id.id)]
        if wizard.date_from:
            domain += [('booking_date', '>=', wizard.date_from)]
        if wizard.date_to:
            domain += [('booking_date', '<=', wizard.date_to)]

        appointments = self.env['hospital.appointment'].search(domain)

        sheet = workbook.add_worksheet("Appointments")
        bold = workbook.add_format({'bold': True})
        sheet.set_column('D:D', 10)
        sheet.set_column('E:E', 25)
        row = 3
        col = 3
        sheet.write(row, col, 'Reference', bold)
        sheet.write(row, col + 1, 'Patient Name', bold)
        for appointment in appointments:
            row += 1
            sheet.write(row, col, appointment.name)
            sheet.write(row, col + 1, appointment.patient_id.name)
