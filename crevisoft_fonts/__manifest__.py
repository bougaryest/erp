# -*- coding: utf-8 -*-
{
    'name': "Crevisoft Fonts",

    'summary': """
        Crevisoft Fonts""",

    'description': """
        Crevisoft Fonts
    """,

    'author': "Crevisoft Corporate",
    'website': "https://www.crevisoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web'],
    # only loaded in demonstration mode
    'assets': {
        'web.report_assets_common': [
            '/crevisoft_fonts/static/src/less/fonts.css'
        ],
    }
}
