# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    building_no = fields.Char(string="Building No", copy=False)
    district = fields.Char(string="District", copy=False)
    postal_code = fields.Char(string="Postal Code", copy=False)
    additional_no = fields.Char(string="Additional No", copy=False)
    other_id = fields.Char(string="Other ID", copy=False)

    def _formatting_address_fields(self):
        res = super(ResPartner, self)._formatting_address_fields()
        res += ['building_no', 'district', 'postal_code', 'additional_no', 'other_id']
        return res
    #


