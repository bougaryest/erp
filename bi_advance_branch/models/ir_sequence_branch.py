# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResBranchIn(models.Model):
    _inherit = 'res.branch'

    prefix = fields.Char('Branch Sequence Prefix')
    apply_prefix = fields.Boolean('Apply Branch Sequence Prefix ??')
    branch_logo = fields.Binary('Branch Logo', attachment=True)

    _sql_constraints = [
        ('prefix_branch_uniq', 'unique (prefix)', _('The prefix per branch must be unique !')),
    ]


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        result = super(SaleOrderInherit, self).create(vals)
        if result.branch_id:
            if result.branch_id.apply_prefix:
                result.write({
                    'name' : result.branch_id.prefix + '-' + result.name
                })

        return result

    def write(self, vals):
        result = super(SaleOrderInherit, self).write(vals)
        if vals.get('branch_id'):
            if vals.get('branch_id') != False:
                branch = self.env['res.branch'].search([('id','=',vals.get('branch_id'))])
                if branch.apply_prefix:
                    count =0 
                    for rec in str(self.name):
                        if rec == '-':
                            count+=1       
                    if count != 0:        
                        val_list = self.name.split('-')
                        val_list[0] = branch.prefix
                        prefix = branch.prefix
                        suffix = val_list[1]
                        self.update({
                            'name' : prefix + '-' + suffix
                        })
                        
                    else:
                        self.update({
                            'name' : branch.prefix + '-' + self.name
                        })
                        
                else:
                    count =0 
                    for rec in str(self.name):
                        if rec == '-':
                            count+=1
                    if count != 0:        
                        val_list = self.name.split('-')
                        suffix = val_list[1]
                        self.update({
                            'name' :  suffix
                        })        
        return result    


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        result = super(PurchaseOrderInherit, self).create(vals)
        if result.branch_id:
            if result.branch_id.apply_prefix:
                result.write({
                    'name' : result.branch_id.prefix + '-' + result.name
                })
        return result

    def write(self, vals):
        result = super(PurchaseOrderInherit, self).write(vals)
        if vals.get('branch_id'):
            branch = self.env['res.branch'].search([('id','=',vals.get('branch_id'))])
            if branch.apply_prefix:
                count =0 
                for rec in str(self.name):
                    if rec == '-':
                        count+=1
                if count != 0:        
                    val_list = self.name.split('-')
                    val_list[0] = branch.prefix
                    prefix = branch.prefix
                    suffix = val_list[1]
                    self.update({
                        'name' : prefix + '-' + suffix
                    })
                else:
                    self.update({
                        'name' : branch.prefix + '-' + self.name
                    })
            else:
                count =0 
                for rec in str(self.name):
                    if rec == '-':
                        count+=1
                if count != 0:        
                    val_list = self.name.split('-')
                    suffix = val_list[1]
                    self.update({
                        'name' :  suffix
                    })        
                        

        return result    


class PickingInherit(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        result = super(PickingInherit, self).create(vals)
        if result.branch_id:
            if result.branch_id.apply_prefix:
                result.write({
                    'name' : result.branch_id.prefix + '-' + result.name
                })
        return result

    def write(self, vals):
        result = super(PickingInherit, self).write(vals)
        if vals.get('branch_id'):
            branch = self.env['res.branch'].search([('id','=',vals.get('branch_id'))])
            if branch.apply_prefix:
                count =0 
                for rec in str(self.name):
                    if rec == '-':
                        count+=1
                if count != 0:        
                    val_list = self.name.split('-')
                    val_list[0] = branch.prefix
                    prefix = branch.prefix
                    suffix = val_list[1]
                    self.update({
                        'name' : prefix + '-' + suffix
                    })
                else:
                    self.update({
                        'name' : branch.prefix + '-' + self.name
                    })
            else:
                count =0 
                for rec in str(self.name):
                    if rec == '-':
                        count+=1
                if count != 0:        
                    val_list = self.name.split('-')
                    suffix = val_list[1]
                    self.update({
                        'name' :  suffix
                    })        
                        

        return result    

class AccountMoveInherit(models.Model):
    _inherit = "account.move"



    def _post(self, soft=True):
        result = super(AccountMoveInherit, self)._post()
        for rec in self:
            if rec.name and rec.branch_id:
                if rec.branch_id.apply_prefix:
                    string = str(rec.name)
                    if string.split('-'):
                        rec.name = string.split('-')[-1]
                    rec.name = rec.branch_id.prefix + '-' + rec.name

                    rec.payment_reference = rec.name
                    for record in rec.line_ids:
                        if rec.move_type in ['out_invoice','out_receipt','out_refund']:
                            if record.debit >0 and record.credit == 0:
                                record.update({'name':rec.name})
                        elif rec.move_type in ['in_invoice','in_receipt','in_refund']:
                            if record.credit >0 and record.debit == 0:
                                record.update({'name':rec.name})                  
        return result


class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"

    def action_post(self):    
        result = super(AccountPaymentInherit, self).action_post()
        if self.name and self.branch_id:
            if self.branch_id.apply_prefix:
                string = str(self.name)
                if string.split('-'):
                    self.name = string.split('-')[-1]
                else:
                    pass
                self.name = self.branch_id.prefix + '-' + self.name 
        
        return result
