# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'


    branch_id = fields.Many2one('res.branch', string="Branch", domain="[('company_id', '=',company_id)]",
                                check_company=True)