# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class purchase_order(models.Model):

    _inherit = 'purchase.order.line'

    
    def _prepare_account_move_line(self, move=False):
        result = super(purchase_order, self)._prepare_account_move_line(move)
        result.update({
            'branch_id' : self.order_id.branch_id.id or False,
            
        })
        return result


    @api.model
    def default_get(self, default_fields):
        res = super(purchase_order, self).default_get(default_fields)
        branch_id = False
        if self._context.get('branch_id'):
            branch_id = self._context.get('branch_id')
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({'branch_id': branch_id})
        return res

    branch_id = fields.Many2one('res.branch', string="Branch", domain="[('company_id', '=',company_id)]",
                                check_company=True)

    def _prepare_stock_moves(self, picking):
        result = super(purchase_order, self)._prepare_stock_moves(picking)

        branch_id = False
        if self.branch_id:
            branch_id = self.branch_id.id
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id

        for res in result:
            res.update({'branch_id' : branch_id})

        return result


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    
    @api.model
    def default_get(self,fields):
        res = super(PurchaseOrder, self).default_get(fields)
        branch_id = picking_type_id = False

        allowed_branch_ids = self._context.get("allowed_branch_ids", [])
        if allowed_branch_ids:
            branch_id = allowed_branch_ids[0]
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id

        if branch_id:
            branched_warehouse = self.env['stock.warehouse'].search([('branch_id', '=', branch_id)])
            if branched_warehouse:
                picking_type_id = branched_warehouse[0].in_type_id.id
        else:
            picking = self._default_picking_type()
            picking_type_id = picking.id

        res.update({
            'branch_id': branch_id,
            'picking_type_id': picking_type_id
        })

        return res

    branch_id = fields.Many2one('res.branch', string="Branch", domain="[('company_id', '=',company_id)]",
                                check_company=True)

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id and self.branch_id.company_id.id != self.company_id.id:
            self.branch_id = False

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        branch_id = False
        if self.branch_id:
            branch_id = self.branch_id.id
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({
            'branch_id' : branch_id
        })
        return res


    def _prepare_invoice(self):
        result = super(PurchaseOrder, self)._prepare_invoice()
        branch_id = False
        if self.branch_id:
            branch_id = self.branch_id.id
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id

        result.update({
                
                'branch_id' : branch_id
            })
        
        return result
    def action_view_invoice(self, invoices=False):
        '''
        This function returns an action that display existing vendor bills of given purchase order ids.
        When only one found, show the vendor bill immediately.
        '''

        result = super(PurchaseOrder, self).action_view_invoice(invoices)

        branch_id = False
        if self.branch_id:
            branch_id = self.branch_id.id
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id

        result.update({

            'branch_id': branch_id
        })
        return result

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        allowed_branch_ids = self._context.get("allowed_branch_ids", [])
        if allowed_branch_ids and self.branch_id and self.branch_id.id not in allowed_branch_ids:
            self.branch_id = allowed_branch_ids[0]
            raise ValidationError(_("Please select active branch only. Other may create the Multi branch issue. \n\ne.g: If you wish to add other branch then Switch branch from the header and set that."))


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'


    @api.model
    def default_get(self,fields):
        res = super(PurchaseRequisition, self).default_get(fields)
        branch_id = picking_type_id = False

        allowed_branch_ids = self._context.get("allowed_branch_ids", [])
        if allowed_branch_ids:
            branch_id = allowed_branch_ids[0]
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id

        if branch_id:
            branched_warehouse = self.env['stock.warehouse'].search([('branch_id', '=', branch_id)])
            if branched_warehouse:
                picking_type_id = branched_warehouse[0].in_type_id.id
        else:
            picking = self._default_picking_type()
            picking_type_id = picking.id

        res.update({
            'branch_id': branch_id,
            'picking_type_id': picking_type_id
        })

        return res

    branch_id = fields.Many2one('res.branch', string="Branch", domain="[('company_id', '=',company_id)]",
                                check_company=True)

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id and self.branch_id.company_id.id != self.company_id.id:
            self.branch_id = False



