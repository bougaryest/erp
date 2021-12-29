# -*- coding: utf-8 -*-
{
    'name': "Bank Advanced",
    'description': """
    Bank Advanced
    """,
    'author': "Crevisoft Corporate",
    'website': "https://www.crevisoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting & Finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant', 'web'],

    # always loaded
    'data': [
         'views/res_bank_view.xml',
    ]
}
