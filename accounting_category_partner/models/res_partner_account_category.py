# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartnerAccountCategory(models.Model):
    _name = 'res.partner.account.category'
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    name = fields.Char(string='Name', required=True, translate=True)
    account_payable_id = fields.Many2one('account.account', string="Account Payable",
                                         domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
                                         required=True)
    account_receivable_id = fields.Many2one('account.account', string="Account Receivable",
                                            domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
                                            required=True)
    apply_to_customer = fields.Boolean("Apply to Customer", default=True, copy=False)
    apply_to_vendor = fields.Boolean("Apply to Vendor", default=True, copy=False)

    complete_name = fields.Char("Complete Name", compute="_compute_complete_name", recursive=True, store=True)
    parent_id = fields.Many2one("res.partner.account.category", "Parent", index=True,
                                ondelete="cascade")
    parent_path = fields.Char(index=True)

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for partner_category in self:
            if partner_category.parent_id:
                partner_category.complete_name = "%s / %s" % (
                    partner_category.parent_id.complete_name, partner_category.name)
            else:
                partner_category.complete_name = partner_category.name

    def unlink(self):
        partner_obj = self.env['res.partner']
        config_parameters = self.env["ir.config_parameter"].sudo()

        customer_account_category_id = config_parameters.get_param(
            'accounting_category_partner.customer_account_category_id', False)
        vendor_account_category_id = config_parameters.get_param(
            'accounting_category_partner.vendor_account_category_id', False)

        config_customer_account_category_id = customer_account_category_id and eval(
            customer_account_category_id) or False
        config_vendor_account_category_id = vendor_account_category_id and eval(vendor_account_category_id) or False

        account_categories = []
        if config_customer_account_category_id or config_vendor_account_category_id:
            if config_customer_account_category_id:
                account_categories.append(config_customer_account_category_id)

            if config_vendor_account_category_id:
                account_categories.append(config_vendor_account_category_id)

        for partner_account_category in self:
            # check used in configuration or not
            if account_categories and partner_account_category.id in account_categories:
                raise ValidationError(_(
                    'You cannot delete a partner category %s which is already used in settings' % partner_account_category.name))

            # check related with partners or not
            partners = partner_obj.search([('partner_account_category_id', '=', partner_account_category.id)])
            if partners:
                raise ValidationError(
                    _(
                        'You cannot delete a partner category %s which is related to Partners' % partner_account_category.name))
        return super(ResPartnerAccountCategory, self).unlink()
