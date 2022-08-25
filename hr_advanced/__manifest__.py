# -*- coding: utf-8 -*-
{
    'name': "HR Advanced",

    'summary': """
        HR Advanced""",

    'description': """
HR Advanced
===================
It consist of:

1) Allowances 
2) Number and Age Employee
3) Employee Access Own Profile
    """,

    'author': "Crevisoft Corporate",
    'website': "https://www.crevisoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll_account', 'hr_holidays', 'hr_timesheet'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/medical_insurance_type_data.xml',
        'data/ir_sequence.xml',
        'views/hr_contract_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_medical_insurance_type_view.xml',
        'views/hr_leave_type_views.xml',
        'views/gosi_view.xml',
        'views/res_config_views.xml',
        'views/menu.xml',
    ]
}
