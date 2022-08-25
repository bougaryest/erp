# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    building_no = fields.Char(related='partner_id.building_no', string="Building No", store=True, readonly=False)
    district = fields.Char(related='partner_id.district', string="District", store=True, readonly=False)
    postal_code = fields.Char(related='partner_id.postal_code', string="Postal Code", store=True, readonly=False)
    additional_no = fields.Char(related='partner_id.additional_no', string="Additional No", store=True, readonly=False)
    other_id = fields.Char(related='partner_id.other_id', string="Other ID", store=True, readonly=False)



