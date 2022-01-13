# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    branch_id = fields.Many2one('res.branch', string="Branch", domain="[('company_id', '=',company_id)]",
                                check_company=True)


    @api.model
    def default_get(self, default_fields):

        res = super(StockWarehouse, self).default_get(default_fields)
        branch_id = False
        allowed_branch_ids = self._context.get("allowed_branch_ids", [])
        if allowed_branch_ids:
            branch_id = allowed_branch_ids[0]
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({
            'branch_id': branch_id
        })
        return res


    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id and self.branch_id.company_id.id != self.company_id.id:
            self.branch_id = False

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        allowed_branch_ids = self._context.get("allowed_branch_ids", [])
        if allowed_branch_ids and self.branch_id and self.branch_id.id not in allowed_branch_ids:
            self.branch_id = allowed_branch_ids[0]
            raise Warning(
                _("Please select active branch only. Other may create the Multi branch issue. \n\ne.g: If you wish to add other branch then Switch branch from the header and set that."))


class StockPickingTypeIn(models.Model):
    _inherit = 'stock.picking.type'

    branch_id = fields.Many2one('res.branch',related='warehouse_id.branch_id', store=True,)
