{
    'name': "Delivery Templates",
    'version': '0.1',
    'summary': 'Delivery Templates',
    'category': 'stock',
    'description': """Delivery Templates Module""",
    'author': "Crevisoft Corporate",
    'website': "https://www.crevisoft.com",

    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_template_views.xml',
        'views/stock_picking_view.xml',
    ],
}