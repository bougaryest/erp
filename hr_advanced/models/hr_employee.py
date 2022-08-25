# -*- coding: utf-8 -*-

from datetime import date

from odoo import models, fields, api


class Employee(models.Model):
    _inherit = 'hr.employee'

    age = fields.Integer(string='Age', compute='_compute_employee_age')
    ref = fields.Char(string='Reference', readonly=True, copy=False , groups="hr.group_hr_user")
    emp_id = fields.Char(string="EMP ID", copy=False, tracking=True , groups="hr.group_hr_user")
    arabic_name = fields.Char(string="Arabic Name", copy=False, tracking=True , groups="hr.group_hr_user")
    iqama_no = fields.Char(string="IQAMA NO", copy=False, tracking=True , groups="hr.group_hr_user")
    iqama_expiry_date = fields.Date(string="IQAMA Expiry date", copy=False, tracking=True , groups="hr.group_hr_user")
    gosi = fields.Integer(string="GOSI", copy=False, tracking=True , groups="hr.group_hr_user")
    position_iqama = fields.Char(string="Position - IQAMA", copy=False, tracking=True , groups="hr.group_hr_user")
    insurance_class = fields.Char(string="Insurance class", copy=False, tracking=True , groups="hr.group_hr_user")
    sponsorship = fields.Selection([
        ('under_guarantee', 'under Guarantee'),
        ('out_of_guarantee', 'out of Guarantee')],  string='Sponsorship', index=True, copy=False,
        tracking=True , groups="hr.group_hr_user")

    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank')],  string='Payment Type', index=True, copy=False, tracking=True , groups="hr.group_hr_user")

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hr.employee')
        return super(Employee, self).create(vals)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = ['|', ('name', operator, name), ('ref', operator, name)] + args
        recs = self.search(domain + args, limit=limit)
        return recs.name_get()

    @api.depends('birthday')
    def _compute_employee_age(self):
        age = False
        if self.birthday:
            dob = self.birthday
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        self.age = age
