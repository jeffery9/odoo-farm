{
    'name': 'Farm ESG Compliance',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'ESG Compliance Management for Farm Operations (Epic 101)',
    'description': """
ESG Compliance module for Odoo 19 Farm Management System - Epic 101 Implementation.
- Carbon neutral certification and reporting
- Sustainable agriculture practice certification
- ESG data governance and quality control
- Triple bottom line metrics management (US-101-01)
- Multi-scale sustainable business model design (US-101-02)
- Sustainable supply chain management (US-101-04)
- Sustainable product lifecycle management (US-101-05)
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'farm_esg',
        'farm_esg_environmental',
        'account',
        'farm_agri_science',
        'farm_esg_circular',  # For circular economy integration
        'farm_ai_decision',  # For AI recommendations and decision making
        'farm_supply_analytics',  # For supply chain analytics
        'farm_supply_logistics',  # For supply chain logistics
        'farm_financial_core',  # For financial metrics
        'farm_risk',  # For risk assessment
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/esg_compliance_sequences.xml',
        'views/esg_compliance_views.xml',
        'views/triple_bottom_line_metrics_views.xml',
        'views/sustainable_business_model_views.xml',
        'views/sustainable_supply_chain_views.xml',
        'views/sustainable_product_lifecycle_views.xml',
        'views/supply_chain_carbon_tracking_views.xml',
        'views/carbon_neutral_management_views.xml',
        'views/external_esg_marketplace_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}