# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    gosi_id = fields.Many2one("default.gosi", string="Default GOSI", config_parameter="hr_advanced.gosi_id")

