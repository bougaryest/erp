# -*- coding: utf-8 -*-
{
    'name': "E-Invoice Egypt",

    'summary': """
        E-Invoice Egypt""",

    'description': """
        E-Invoice Egypt
    """,

    'author': "Crevisoft Corporate",
    'website': "https://www.crevisoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
        'views/res_currency_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/uom_views.xml',
        'views/account_tax_views.xml',
        'views/account_move_views.xml',
        'views/taxpayer_activity_code_views.xml'
    ],
}
