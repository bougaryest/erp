# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountTax(models.Model):
    _inherit = "account.tax"

    eta_code = fields.Char(string="Code", copy=False)
    eta_sub_type_code = fields.Char(string="SubType Code", copy=False)
