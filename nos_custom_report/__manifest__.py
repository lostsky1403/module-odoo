# -*- coding: utf-8 -*-
#############################################################################
{
    'name': 'Nos Custom Report',
    'version': '17.0.1.0.0',
    'category': 'Uncategorized',
    'summary': """Generate PDF Report of Custom""",
    'description': """Custom Report From Nuyostech""",
    'author': 'Nuyostech',
    'company': 'Nuyostech',
    'maintainer': 'Nuyostech',
    'website': "https://www.nuyostech.com",
    'depends': ['base','sale','sale_management', 'account','purchase'],
    'data': [
        'report/nos_sale_order_reports.xml',
        'report/nos_sale_order_template.xml',
        'report/nos_purchase_order_template.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
