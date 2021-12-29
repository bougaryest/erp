# -*- coding: utf-8 -*-
{
    'name': "Electronic Invoice",
    'description': """
    Electronic Invoice
    """,
    'author': "Crevisoft Corporate",
    'website': "https://www.crevisoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting & Finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant', 'web','bank_advanced'],

    # always loaded
    'data': [
        'views/account_invoice_view.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/report_tax_invoice.xml',
        # 'views/res_bank_view.xml',
        'views/templates.xml',
    ]
}
