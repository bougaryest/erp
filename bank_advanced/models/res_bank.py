from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    iban = fields.Char("IBAN")
    swift_code = fields.Char("Swift Code")

