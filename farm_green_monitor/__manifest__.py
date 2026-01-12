{
    'name': 'Farm Green Monitoring (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Fertilizer/Pesticide Reduction Assessment',
    'description': """
        Monitors and assesses fertilizer and pesticide reduction targets and trends [US-18-06].
        - Calculates per-unit-area usage of fertilizers and pesticides.
        - Generates reduction trend charts for government inspection.
        - Provides early warnings if usage increases year-over-year.
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_operation', 'farm_supply', 'farm_sustainability'],
    'data': [
        'security/ir.model.access.csv',
        'report/reduction_report_templates.xml',
        'report/reduction_reports.xml',
        'views/green_monitor_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
