from odoo import models, fields


class PatientReportWizard(models.TransientModel):
    _name = 'patient.report.wizard'
    _description = "Patient Report Wizard"

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    age = fields.Integer()

    def action_print_report(self):
        form = self.read()[0]
        data = {
            'gender': form.get('gender'),
            'age': form.get('age'),
        }

        return self.env.ref('om_hospital.report_all_patient').report_action(self, data=data)
