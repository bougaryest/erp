# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    @api.onchange('acquisition_date','first_depreciation_date')
    def _check_acquisition_date(self):
        for asset in self:
            if asset.acquisition_date < asset.first_depreciation_date:
                raise ValidationError(_('Acquisition Date Must Be Greater than Start Depreciating'))





