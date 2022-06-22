# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class HrContract(models.Model):
    _inherit = "hr.contract"


    l10n_sa_housing_allowance = fields.Monetary(string='Saudi Housing Allowance')
    l10n_sa_transportation_allowance = fields.Monetary(string='Saudi Transportation Allowance')
    l10n_sa_other_allowances = fields.Monetary(string='Saudi Other Allowances')
    l10n_sa_number_of_days = fields.Integer(string='Saudi Number of Days',
                                            help='Number of days of basic salary to be added to the end of service provision per year')
    l10n_sa_company_country_code = fields.Char(related='company_country_id.code', string='Saudi Company Country Code')
