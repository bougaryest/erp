# -*- coding: utf-8 -*-

from odoo import models, fields


# class ResCompany(models.Model):
#     _inherit = 'res.company'
#
#     arabic_name = fields.Char()
#     address = fields.Text( )
#
# class BaseDocumentLayout(models.TransientModel):
#     _inherit = 'base.document.layout'
#
#     arabic_name = fields.Char(related='company_id.arabic_name', readonly=True)
#     address = fields.Text(related='company_id.address', readonly=True)
#     company_registry = fields.Char(related='company_id.company_registry', readonly=True)
#     street = fields.Char(related='company_id.street', readonly=True)
#     city = fields.Char(related='company_id.city', readonly=True)
#     zip = fields.Char(related='company_id.zip', readonly=True)
#
#
