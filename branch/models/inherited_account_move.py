# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from odoo.exceptions import Warning
from odoo.tools.sql import column_exists, create_column


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountMove, self).default_get(default_fields)
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

    branch_id = fields.Many2one('res.branch', string="Branch", domain="[('company_id', '=',company_id)]",
                                check_company=True)

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


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountMoveLine, self).default_get(default_fields)
        branch_id = False

        allowed_branch_ids = self._context.get("allowed_branch_ids", [])
        if allowed_branch_ids:
            branch_id = allowed_branch_ids[0]
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id

        if self.move_id.branch_id:
            branch_id = self.move_id.branch_id.id
        res.update({'branch_id': branch_id})
        return res

    branch_id = fields.Many2one('res.branch', string="Branch", related="move_id.branch_id", store=True)
