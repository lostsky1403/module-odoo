# -*- coding: utf-8 -*-
#############################################################################
{
    'name': 'Nos Custom Report',
    'version': '18.0.1.0.0',
    'category': 'Reporting',
    'summary': """Generate PDF Report of Custom""",
    'description': """Custom Report From Nuyostech""",
    'author': 'Nuyostech',
    'company': 'Nuyostech',
    'maintainer': 'Nuyostech',
    'website': "https://www.nuyostech.com",
    'depends': ['base', 'sale', 'sale_management', 'account', 'purchase'],
    'data': [
        'report/nos_sale_order_reports.xml',
        'report/nos_sale_order_template.xml',
        'report/nos_purchase_order_template.xml',
    ],
    'assets': {
        'web.report_assets_pdf': [
            # Add custom CSS files here if needed
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}