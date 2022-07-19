# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    branch_ids = fields.Many2many('res.branch', string="Allowed Branch", domain="[('company_id', 'in',company_ids)]")
    branch_id = fields.Many2one('res.branch', string="Branch", domain="[('id', 'in',branch_ids)]")


    @api.onchange('company_ids')
    def onchange_company_ids(self):
        branch_ids = []
        allow_branch_ids = self.env['res.branch'].search([('company_id', 'in', self.company_ids.ids)]).ids

        if allow_branch_ids:
            for branch in self.branch_ids:
                if branch._origin.id in allow_branch_ids:
                    branch_ids.append(branch._origin.id)

        self.branch_ids = branch_ids and [(6, 0, branch_ids)] or False

        if self.branch_id.id not in self.branch_ids.ids:
            self.branch_id = False

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id and self.branch_id.company_id.id != self.company_id.id:
            self.branch_id = False

    def write(self, values):
        if 'branch_id' in values or 'branch_ids' in values:
            self.env['ir.model.access'].call_cache_clearing_methods()
            self.env['ir.rule'].clear_caches()
            # self.has_group.clear_cache(self)
        user = super(ResUsers, self).write(values)
        return user
