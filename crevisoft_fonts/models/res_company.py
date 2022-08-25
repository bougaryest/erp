# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    font = fields.Selection(selection_add=[
        ('Tajawal', 'Tajawal'),
        ('Readex Pro', 'Readex Pro'),
        ('Noto Naskh Arabic', 'Noto Naskh Arabic'),
        ('Noto Sans Arabic', 'Noto Sans Arabic'),
    ])
