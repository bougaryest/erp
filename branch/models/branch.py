# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.osv import expression

class ResBranch(models.Model):
    _name = 'res.branch'
    _description = 'Branch'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    company_id = fields.Many2one('res.company', required=True)
    telephone = fields.Char(string='Telephone No')
    address = fields.Text('Address')
    vat = fields.Char(string="Tax ID")
    company_registry = fields.Char(string="Company Registry")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    website = fields.Char(string="Website")


    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State',domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country')

    building_no = fields.Char(string="Building No", copy=False)
    district = fields.Char(string="District", copy=False)
    postal_code = fields.Char(string="Postal Code", copy=False)
    additional_no = fields.Char(string="Additional No", copy=False)
    other_id = fields.Char(string="Other ID", copy=False)
    picking_type_ids = fields.Many2many("stock.picking.type", string="Operation Type")
    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouse')




    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        branchs = super(ResBranch, self)._name_search(name, args=None, operator='ilike', limit=100, name_get_uid=None)
        if not branchs:
            branchs = self._search(expression.AND([[('code', operator, name)], args]), limit=limit, access_rights_uid=name_get_uid)
        return branchs









    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            self.street = self.company_id.name
            self.street2 = self.company_id.street2
            self.zip = self.company_id.zip
            self.city = self.company_id.city
            self.building_no = self.company_id.building_no
            self.district = self.company_id.district
            self.postal_code = self.company_id.postal_code
            self.additional_no = self.company_id.additional_no
            self.other_id = self.company_id.other_id
            self.state_id = self.company_id.state_id.id
            self.country_id = self.company_id.country_id.id
            self.vat = self.company_id.vat
            self.company_registry = self.company_id.company_registry


