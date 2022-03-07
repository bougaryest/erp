# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_template_id = fields.Many2one("stock.picking.delivery.template", string="Delivery Template", tracking=True)

    @api.onchange('picking_type_id')
    def onchange_template_picking_type_id(self):
        if self.picking_type_code != 'outgoing':
            self.delivery_template_id = False

    @api.onchange("delivery_template_id")
    def onchange_delivery_template_id(self):
        lines = [(3, stock_move_line.id) for stock_move_line in
                 self.move_ids_without_package.filtered(lambda l: l.delivery_template_id)]
        for template_line in self.delivery_template_id.lines:
            vals = {
                'name': template_line.product_id.name,
                'product_id': template_line.product_id.id,
                'product_uom_qty': template_line.quantity,
                'quantity_done': template_line.quantity,
                'product_uom': template_line.product_id.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'delivery_template_id': self.delivery_template_id.id,
            }
            lines.append((0, 0, vals))

        self.move_ids_without_package = lines

    def _prepare_stock_move(self):
        stock_warehouse_obj = self.env["stock.warehouse"]
        delivery_template = self.delivery_template_id
        picking_type = delivery_template.picking_type_id
        partner = self.partner_id
        product = delivery_template.product_id

        # get source location
        if picking_type.default_location_src_id:
            location_id = picking_type.default_location_src_id.id
        elif partner:
            location_id = partner.property_stock_supplier.id
        else:
            _, location = stock_warehouse_obj._get_partner_locations()
            location_id = location.id

        # get destination location
        if picking_type.default_location_dest_id:
            location_dest_id = picking_type.default_location_dest_id.id
        elif partner:
            location_dest_id = partner.property_stock_customer.id
        else:
            location_dest, _ = stock_warehouse_obj._get_partner_locations()
            location_dest_id = location_dest.id

        vals = {
            "picking_type_id": picking_type.id,
            "partner_id": partner and partner.id or False,
            "date": self.date,
            "origin": self.name,
            "location_id": location_id,
            "location_dest_id": location_dest_id,
            "company_id": self.company_id.id,
            "move_ids_without_package": [(0, 0, {
                "product_id": product.id,
                "product_uom_qty": 1,
                "product_uom": product.uom_id.id,
                "description_picking": self.name,
                "location_id": location_id,
                "location_dest_id": location_dest_id,
                "name": self.name,
                "origin": product.name
            })]
        }
        return vals

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for picking in self.filtered(lambda pick: pick.delivery_template_id):
            move_product_ids = picking.move_ids_without_package.mapped("product_id").ids

            for product in picking.delivery_template_id.lines.mapped("product_id"):
                if product.id not in move_product_ids:
                    raise UserError(_("Missing product %s for delivery template %s") % (
                        product.display_name, picking.delivery_template_id.name))

            if picking.delivery_template_id.picking_type_id:
                self.create(picking._prepare_stock_move())
            return res


class StockMove(models.Model):
    _inherit = "stock.move"

    delivery_template_id = fields.Many2one('stock.picking.delivery.template', string="Delivery Template")
