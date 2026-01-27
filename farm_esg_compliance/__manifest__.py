{
    'name': 'Farm ESG Compliance',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'ESG Compliance, Subsidies and Sustainability Management',
    'description': """
        ESG Compliance module for Odoo 19.
        - Subsidy Tracking and Management [US-56-01]
        - Biodiversity Monitoring [US-56-02]
        - Export Compliance Checks [US-56-03]
        - Sustainability Certification Management [US-56-04]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['farm_esg', 'farm_esg_environmental', 'account', 'farm_agri_science'],
    'data': [
        'security/ir.model.access.csv',
        'views/esg_compliance_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}