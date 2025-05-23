# -*- coding: utf-8 -*-
{
    'name': 'Approval Order',
    'version': '18.0.1.0.0',  # Updated version format for Odoo 18
    'category': 'Sales/Sales',
    'license': 'LGPL-3',  # Updated license format
    'images': ['static/description/icon.png'],
    'depends': ['base', 'sale_management', 'purchase'],
    'data': [
        'security/sale_security.xml',  # Move security files first
        'security/ir.model.access.csv',
        'data/approve_mail_template.xml',
        'data/refuse_mail_template.xml',
        'wizard/sale_order_refuse_wizard_view.xml',
        'views/sale_view.xml',
        'views/purchase_view.xml'
    ],
    'support': 'dev@nuyostech.com',
    'author': 'Nuyostech',
    'website': 'https://nuyostech.com',
    'summary': 'Approval Sales Order',
    'description': '''
Added Director Approval Start Range, Stop Range 
''',
    'installable': True,
    'auto_install': False,
    'application': False,
}