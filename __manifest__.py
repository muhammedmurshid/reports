{
    'name': 'Reports',
    'version': '1.0.0',
    'summary': 'Reports',
    'description': """
        A more detailed description of the module.
    """,
    'author': 'Murshid',
    'website': 'https://www.yourwebsite.com',
    'category': 'Specific Category',
    'license': 'LGPL-3',
    'depends': [
        'base', 'website', 'openeducat_core', 'fee_collection_17', 'custom_leads'  # List of module dependencies

        # Add other module dependencies here
    ],
    'data': [
        'security/ir.model.access.csv',  # Access rights
        # 'security/groups.xml',
        # 'security/ir.model.access.csv',
        'views/invoice_report.xml',
        'views/quick_pay_report.xml',
        # 'views/payment.xml',
        # 'views/payment_web_form.xml',
        'views/receipt.xml',
        'views/lead.xml',
        'views/ancillary_report.xml',
        'views/tax_report.xml',
        'views/wallet_report.xml',
        'views/receipt_report.xml',
        'views/credit_note.xml'

    ],
    'assets': {
        'web.assets_backend': [

            '/reports/static/src/css/styles.css',

        ],
    },

    'installable': True,
    'application': False,
    'auto_install': False,

}
