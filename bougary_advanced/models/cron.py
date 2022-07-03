from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.quant'

    def quant_unlink(self):
        for line in self.env['stock.quant'].search([]):
            line.sudo().unlink()