# -*- coding: utf-8 -*-
from odoo import fields, models

import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    total_discount = fields.Float(string="Total Discount", compute="_compute_discount")
    confirm_date = fields.Datetime(string="Confirm Date", copy=False)
    po_no = fields.Char(copy=False)
    pay_type = fields.Selection(selection=[('cash', 'Cash Sales'), ('deferred', 'Deferred Sales'), ],required=True,)

    def amount_in_words(self, lang, amount):
        return self.company_id.currency_id.with_context(lang=lang).amount_to_text(amount)


    def action_post(self):
        res = super(AccountMove, self).action_post()
        for move in self:
            move.confirm_date = datetime.datetime.now()
        return res



    def _compute_discount(self):
        for move in self:
            discount = 0.0
            for line in move.invoice_line_ids:
                discount += (line.quantity * line.price_unit) * (line.discount or 0.0) / 100.0
            move.total_discount = discount




