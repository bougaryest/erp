# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class HrContract(models.Model):
    _inherit = "hr.contract"

    l10n_sa_company_country_code = fields.Char(related='company_country_id.code', string='Saudi Company Country Code')
