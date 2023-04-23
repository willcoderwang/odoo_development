from odoo import fields, models, api


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False
    # if _log_access = False, columns(create_date, create_uid, write_date, write_uid)
    # will not be generated in the table for this model

    operation_name = fields.Char(string="Name")
    doctor_id = fields.Many2one('res.users')

    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]
