# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockPickingDeliveryTemplate(models.Model):
    _name = "stock.picking.delivery.template"
    _description = "Delivery Templates"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, translate=True, tracking=True, default="Name", index=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, tracking=True)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', domain="[('code', '=', 'incoming')]",
                                      required=True, tracking=True)

    lines = fields.One2many("stock.picking.delivery.template.line", "delivery_template_id", string="Lines")


class StockPickingDeliveryTemplateLine(models.Model):
    _name = "stock.picking.delivery.template.line"
    _description = "Delivery Template lines"

    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1)
    delivery_template_id = fields.Many2one('stock.picking.delivery.template', string='Delivery Template', required=True,
                                           ondelete="cascade")

    @api.constrains('quantity')
    def check_quantity(self):
        for rec in self:
            if rec.quantity < 0:
                raise ValidationError("amount must be positive or equal to zero")
