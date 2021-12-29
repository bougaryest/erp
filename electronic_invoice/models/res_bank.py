from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    iban = fields.Char("IBAN")
    account_no = fields.Many2one("res.partner.bank", string="Account No" )

