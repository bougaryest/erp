# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move'


    move_name = fields.Char(string="", required=False, )


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    partner_account_category_id = fields.Many2one(related="partner_id.partner_account_category_id",
                                                  string="Accounting Category", readonly=True, store=True)
