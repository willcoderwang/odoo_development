import random

from odoo.exceptions import ValidationError

from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _order = 'id desc'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient", ondelete="restrict", tracking=2)
    gender = fields.Selection(related="patient_id.gender", readonly=False)
    appointment_time = fields.Datetime(default=fields.Datetime.now)
    booking_date = fields.Date(default=fields.Date.context_today, tracking=4)
    duration = fields.Float(tracking=3)

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
    doctor_id = fields.Many2one('res.users', tracking=1)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")
    hide_sale_price = fields.Boolean()
    operation_id = fields.Many2one('hospital.operation')
    progress = fields.Integer(compute='_compute_progress', store=True)
    progress_max = fields.Integer(default=100)

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    def write(self, vals):
        res = super().write(vals)
        self.set_line_number()
        return res
    
    def set_line_number(self):
        sl_no = 0
        for line in self.pharmacy_line_ids:
            sl_no += 1
            line.sl_no = sl_no

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can only delete appointment with draft status!"))

        return super().unlink()

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

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://github.com/odoo/odoo',
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_share_whatsapp(self):
        self.ensure_one()
        if not self.patient_id.phone:
            raise ValidationError("Missing phone number in patient record")

        message = f"Hi {self.patient_id.name}, your appointment is: {self.name}, Thank you"
        whatsapp_api_url = f"https://api.whatsapp.com/send?phone={self.patient_id.phone}&text={message}"

        self.message_post(body=message, subject="Whatsapp Message")
        
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url,
        }

    def action_notification(self):
        action = self.env.ref('om_hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Click the following link to go to the patient'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient&view_type=form'
                }],
                'sticky': True,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')],
                }
            }
        }

    def action_sql_query(self):
        cr = self._cr
        query = """ SELECT id, name
                    FROM hospital_patient
                    WHERE id=%s """
        cr.execute(query, (self.patient_id.id,))
        patient = cr.dictfetchone()
        print("patient ====> ", patient)

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            progress = 0
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100

            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    sl_no = fields.Integer('SNO.')
    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string="price", related="product_id.list_price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment')
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal',
                                     currency_field='company_currency_id')
    company_currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
