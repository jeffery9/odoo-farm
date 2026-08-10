{
    'name': 'Farm IoT Management Center',
    'version': '2.1.0',
    'category': 'Industries/Agriculture',
    'summary': 'IoT Management Center - Digital Twin, Global Mapping & Command Orchestration',
    'description': """
        Management Center for Odoo 19 Farm IoT Architecture. [US-203]
        - Centralized IoT Device Mapping & Business Orchestration.
        - Digital Twin Management for Agricultural Assets.
        - Global Command Audit Log (Independent Management Audit).
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['farm_core', 'project', 'agri_iot', 'maintenance', 'stock', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        # 'data/iot_cron_data.xml',
        'views/iot_mapping_views.xml',
        'views/farm_telemetry_views.xml',
        'views/farm_automation_views.xml',
        'views/farm_event_correlation_views.xml',
        
        'views/iiot_device_views.xml',
        'views/digital_twin_views.xml',
        'views/storage_env_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
