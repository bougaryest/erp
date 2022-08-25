# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Hrleavetype(models.Model):
    _inherit = 'hr.leave.type'
    
    is_include_balance = fields.Boolean(string="Include Balance", copy=False)

    @api.onchange('leave_validation_type')
    def onchange_allocation_type(self):
        if self.leave_validation_type == 'no_validation':
            self.is_include_balance = False
