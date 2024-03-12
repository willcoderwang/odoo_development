# -*- coding: utf-8 -*-
from odoo import api, models


class AllPatientReport(models.AbstractModel):
    _name = 'report.om_hospital.report_all_patient_template'
    _description = 'Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('gender'):
            domain += [('gender', '=', data['gender'])]
            
        print(data.get('age'))
        if data.get('age'):
            domain += [('age', '=', data['age'])]

        docs = self.env['hospital.patient'].search(domain)
        return {
            'docs': docs
        }
