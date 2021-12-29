# -*- coding: utf-8 -*-

import json
import logging

import requests
from odoo import models, fields, service, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    e_invoice_environment = fields.Selection([
        ("sit", "SIT"),
        ("uat_preprod", "UAT/PreProd"),
        ("prod", "Production")], default="sit", string="Environment", copy=False)
    e_invoice_api_url = fields.Char(string="API URL", copy=False)
    e_invoice_api_id = fields.Char(string="API ID", copy=False)
    e_invoice_api_secret = fields.Char(string="API Secret", copy=False)

    def check_data_api_required(self):
        if not self.e_invoice_environment:
            raise UserError(_("Environment is required"))

        if not self.e_invoice_api_url:
            raise UserError(_("API URL is required"))

        if not self.e_invoice_api_id:
            raise UserError(_("API ID is required"))

        if not self.e_invoice_api_secret:
            raise UserError(_("API Secret is required"))

        return True

    def test_e_invoice_connection(self):
        self.check_data_api_required()

        data = json.dumps({"params": {
            "environment": self.e_invoice_environment,
            "api_url": self.e_invoice_api_url,
            "api_id": self.e_invoice_api_id,
            "api_secret": self.e_invoice_api_secret,
            "database_id": self.env['ir.config_parameter'].get_param("database.uuid"),
            "company_vat": self.vat,
            "odoo_version": service.common.exp_version()['server_serie']
        }})
        headers = {"Content-type": "application/json", "cache-control": "no-cache"}

        response = requests.request("Post", self.e_invoice_api_url + "/connect/token", data=data, headers=headers)
        
        response_content = json.loads(response.json()["result"])

        if response_content["code"] != 200:
            if response.reason == "NOT FOUND":
                raise UserError(_("URL is not found"))

            raise UserError("%s - %s" % (response_content["code"], response_content["error"]))

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': response_content["message"],
                'type': 'success',
                'sticky': False,
            }
        }
