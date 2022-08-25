# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class DefaultGosi(models.Model):
    _name = 'default.gosi'
    _description = "Default Gosi"

    name = fields.Char(string='Name', translate=True, required=True)

    gosi_percent = fields.Float(string="GOSI percent", copy=False, tracking=True, default="21.5")



    occupational_hazards = fields.Float(string="Occupational Hazards", copy=False, tracking=True,default="2")

    pension_insurance = fields.Float(string="Pension Insurance", copy=False, tracking=True, default="9")
    company_pension_insurance = fields.Float(string="Pension Insurance Company", copy=False, tracking=True,default="9")

    saned = fields.Float(string="Saned", copy=False, tracking=True,default=".75")
    company_saned = fields.Float(string="Saned Company", copy=False, tracking=True,default=".75")
