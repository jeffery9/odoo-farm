{
    'name': 'Farm Subsidy (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Farmland Protection and Grain Subsidy Application',
    'description': """
        Supports Chinese government's farmland protection and grain subsidy policies [US-05-04].
        - Categorization by crop type (early rice, wheat, corn).
        - Generates subsidy application forms matching Ministry of Agriculture and Rural Affairs templates.
        - Integrates with planting area and crop type data from the system.
    """,
    'author': \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    'depends': ['farm_subsidy', 'farm_core', 'farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'report/subsidy_report_templates.xml',
        'report/subsidy_reports.xml',
        'views/subsidy_ch_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
