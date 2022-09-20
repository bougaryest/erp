# -*- coding: utf-8 -*-
from odoo import fields, models,api


class PosOrder(models.Model):
    _inherit = 'pos.order'


    branch_id = fields.Many2one('res.branch', string="Branch", domain="[('company_id', '=',company_id)]",
                                )

    @api.model
    def _process_order(self, order, draft, existing_order):
        res = super(PosOrder, self)._process_order(order, draft, existing_order)
        pos_order = self.env['pos.order'].browse(res)
        pos_order.write({"branch_id": pos_order.config_id.branch_id.id or False})
        return res

