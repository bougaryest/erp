# -*- coding: utf-8 -*-
{
    'name': "E-Invoice KSA - POS | QR Code | POS | ZATCA | VAT | E-Invoice | Tax | Zakat",
    'summary': 'TeleNoc E-Invoice for POS is fully compatible with Odoo standard invoice template.',
    'version': '15.0.1.0.0',
    "category" : "Accounting",
    'description': """
        Electronic invoice KSA - POS
    """,
    'author': "Crevisoft Corporate",
    'website': "https://www.crevisoft.com",
    'images': ['static/description/banner.jpg',
              'static/description/apps_screenshot.jpg'],
    'depends': ['base', 'account', 'point_of_sale','l10n_sa_pos'],
    "data": [],
    'qweb': ['static/src/xml/pos.xml'],
    "application": True,
    'assets': {
        'web.assets_qweb': [
            'pos_sa_invoice/static/src/xml/**/*',
        ],
    },
}
