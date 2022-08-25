# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class HrContract(models.Model):
    _inherit = "hr.contract"


    ref = fields.Char('Reference', readonly=True, copy=False)
    overtime_allowance = fields.Monetary(string="Overtime", copy=False, tracking=True, )
    # transportation_allowance = fields.Monetary(string="Transportation", copy=False, tracking=True)
    food_allowance = fields.Monetary(string="Food", copy=False, tracking=True)
    # housing_allowance = fields.Monetary(string="Housing", copy=False, tracking=True)
    mobile_allowance = fields.Monetary(string="Mobile", copy=False, tracking=True)
    fuel_allowance = fields.Monetary(string="Fuel", copy=False, tracking=True)
    ticket_allowance = fields.Monetary(string="Ticket", copy=False, tracking=True)
    commission_allowance = fields.Monetary(string='Commission', copy=False, tracking=True)
    other_allowance = fields.Monetary(string='Other', copy=False, tracking=True)

    work_permit_fees_deduction = fields.Monetary(string="Work Permit Fees", copy=False, tracking=True)
    leave_deduction = fields.Monetary(string="Leave", copy=False, tracking=True)
    esob_deduction = fields.Monetary(string="End Of Service (ESOB)", copy=False, tracking=True)
    tax_deduction = fields.Monetary(string="Taxes", copy=False, tracking=True)
    tax_deduction_amount = fields.Monetary(string="Taxes Amount", copy=False, tracking=True)

    iqama_fees_deduction = fields.Monetary(string="IQAMA Fees", copy=False, tracking=True)

    gosi_deduction = fields.Float(string="GOSI", copy=False, tracking=True, store=True)
    gosi_suodi = fields.Boolean(string="GOSI  Suodi", copy=False, tracking=True,default=True)
    gosi_percent = fields.Float(string="GOSI percent", copy=False, tracking=True)
    gosi_distributed = fields.Boolean(string="GOSI  Distributed", copy=False, tracking=True)


    occupational_hazards = fields.Float(string="Occupational Hazards", copy=False, tracking=True,)

    pension_insurance = fields.Float(string="Pension Insurance", copy=False, tracking=True, )
    company_pension_insurance = fields.Float(string="Pension Insurance Company", copy=False, tracking=True,)

    saned = fields.Float(string="Saned", copy=False, tracking=True,)
    company_saned = fields.Float(string="Saned Company", copy=False, tracking=True)


    amount_occupational_hazards = fields.Monetary(string="Amount Occupational Hazards", copy=False, tracking=True,  store=True)
    amount_pension_insurance = fields.Monetary(string="Amount Pension Insurance", copy=False, tracking=True, store=True)
    amount_company_pension_insurance = fields.Monetary(string="Amount Pension Insurance", copy=False, tracking=True, store=True)
    amount_saned = fields.Monetary(string="Amount Saned", copy=False, tracking=True, store=True)
    amount_company_saned = fields.Monetary(string="Amount Saned", copy=False, tracking=True, store=True)

    

    medical_insurance_deduction = fields.Float(string="Medical Insurance", copy=False, tracking=True)
    medical_insurance_type_id = fields.Many2one("hr.medical.insurance.type", string="Medical Insurance Type",
                                                copy=False, tracking=True)
    total_wage = fields.Float(string='Total Wage', copy=False, tracking=True)
    wage_day = fields.Float(string="Wage(Day)", copy=False, tracking=True)


    @api.constrains('gosi_percent','occupational_hazards', 'pension_insurance', 'saned','gosi_distributed')
    def _check_gosi_percent(self):
        for contract in self:
            if contract.gosi_percent:
                if  contract.gosi_percent <= 0.0 or contract.gosi_percent > 100:
                    raise ValidationError(_("GOSI percent must be between 0 and 100 and not equal to zero"))

                if not contract.gosi_suodi:
                    if  contract.occupational_hazards <= 0.0 or contract.occupational_hazards > 100:
                        raise ValidationError(_("Occupational Hazards must be between 0 and 100 and not equal to zero"))
                else:
                    if  contract.pension_insurance <= 0.0 or contract.pension_insurance > 100:
                        raise ValidationError(_("Pension Insurance must be between 0 and 100 and not equal to zero"))
                    if  contract.saned <= 0.0 or contract.saned > 100:
                        raise ValidationError(_("Saned must be between 0 and 100 and not equal to zero"))
                    if  contract.company_pension_insurance <= 0.0 or contract.company_pension_insurance > 100:
                        raise ValidationError(_("Company Pension Insurance must be between 0 and 100 and not equal to zero"))
                    if  contract.company_saned <= 0.0 or contract.company_saned > 100:
                        raise ValidationError(_("Company Saned must be between 0 and 100 and not equal to zero"))

            total_gosi = contract.gosi_percent
            total_distributed_gosi = round(contract.occupational_hazards, 2)
            if contract.gosi_suodi:
                total_distributed_gosi += round(contract.pension_insurance + contract.company_pension_insurance + contract.saned + contract.company_saned , 2)
            if total_gosi != total_distributed_gosi:
                raise ValidationError(_("GOSI percent must be equal total GOSI percent distributed"))



    @api.onchange('gosi_suodi')
    def onchange_gosi_suodi(self):
        gosi_id = eval(self.env["ir.config_parameter"].sudo().get_param("hr_advanced.gosi_id", "False"))
        gosi_id = self.env["default.gosi"].browse(gosi_id)
        print(gosi_id)
        if self.gosi_suodi:
            self.gosi_percent = gosi_id.gosi_percent or  False
            self.occupational_hazards = gosi_id.occupational_hazards or  False
            self.company_pension_insurance = gosi_id.company_pension_insurance or  False
            self.pension_insurance = gosi_id.pension_insurance or  False
            self.company_saned = gosi_id.company_saned or  False
            self.saned = gosi_id.saned or  False
        else:
            self.gosi_percent = gosi_id.occupational_hazards or  False
            self.occupational_hazards = gosi_id.occupational_hazards or  False
            self.company_pension_insurance = False
            self.pension_insurance = False
            self.company_saned = False
            self.saned = False



    @api.onchange('occupational_hazards', 'wage')
    def _onchange_occupational_hazards_amount(self):
        for contract in self:
            amount_occupational_hazards = 0.0
            if contract.occupational_hazards and contract.wage:
                amount_occupational_hazards = contract.wage * (contract.occupational_hazards / 100)
            contract.amount_occupational_hazards = amount_occupational_hazards

    @api.onchange('pension_insurance', 'wage')
    def _onchange_pension_insurance_amount(self):
        for contract in self:
            amount_pension_insurance = 0.0
            if contract.pension_insurance and contract.wage:
                amount_pension_insurance = contract.wage *  (contract.pension_insurance/ 100)
            contract.amount_pension_insurance = amount_pension_insurance

    @api.onchange('saned', 'wage')
    def _onchange_saned_amount(self):
        for contract in self:
            amount_saned = 0.0
            if contract.saned and contract.wage:
                amount_saned = contract.wage * (contract.saned / 100)
            contract.amount_saned = amount_saned

    @api.onchange('company_pension_insurance', 'wage')
    def _onchange_amount_company_pension_insurance(self):
        for contract in self:
            amount_company_pension_insurance = 0.0
            if contract.company_pension_insurance and contract.wage:
                amount_company_pension_insurance = contract.wage * (contract.company_pension_insurance / 100)
            contract.amount_company_pension_insurance = amount_company_pension_insurance

    @api.onchange('company_saned', 'wage')
    def _onchange_company_saned(self):
        for contract in self:
            amount_company_saned = 0.0
            if contract.company_saned and contract.wage:
                amount_company_saned = contract.wage * (contract.company_saned / 100)
            contract.amount_company_saned = amount_company_saned

    @api.onchange('gosi_percent', 'wage')
    def _compute_gosi_amount(self):
        for contract in self:
            gosi_deduction = 0.0
            if contract.gosi_percent and contract.wage:
                gosi_deduction = contract.wage * (contract.gosi_percent / 100)
            contract.gosi_deduction = gosi_deduction

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hr.contract')
        return super(HrContract, self).create(vals)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = ['|', ('name', operator, name), ('ref', operator, name)] + args
        recs = self.search(domain + args, limit=limit)
        return recs.name_get()

    @api.onchange('gosi_percent', 'wage')
    def _compute_gosi_amount(self):
        for contract in self:
            gosi_deduction = 0.0
            if contract.gosi_percent and contract.wage:
                gosi_deduction = contract.wage * (contract.gosi_percent / 100)
            contract.gosi_deduction = gosi_deduction

    @api.onchange('tax_deduction', 'wage')
    def _onchange_tax_deduction_amount(self):
        for contract in self:
            tax_amount = 0.0
            if contract.tax_deduction and contract.wage:
                tax_amount = contract.wage * contract.tax_deduction
            contract.tax_deduction_amount = tax_amount

    @api.onchange('medical_insurance_type_id')
    def _onchange_medical_insurance_amount(self):
        self.medical_insurance_deduction = self.medical_insurance_type_id and self.medical_insurance_type_id.amount or 0.0
