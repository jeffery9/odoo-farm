{
    'name': 'Precision Production IoT Integration',
    'summary': 'IoT Integration for Automatic Measurement Data Reading in Precision Production',
    'description': """
Precision Production IoT Integration
===============================

This module enables IoT device integration for automatic reading of measurement data
in precision production processes. It provides real-time data collection from sensors
and devices, supporting various protocols and automatic data validation in the context
of ISA-88 compliant production execution.

Key Features:
- IoT device management and connection
- Real-time measurement data collection
- Automatic validation and deviation detection
- Integration with precision metrology workflows
- Support for multiple sensor types and protocols
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'category': 'Manufacturing/IoT',
    'version': '1.0.0',
    'depends': [
        'base',
        'stock',
        'mrp',
        'agri_iot',  # Required dependency for IIoT device management
        'precision_production',  # Required dependency for precision production functionality
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/iot_device_views.xml',
        'views/iot_sensor_views.xml',
        'views/iot_reading_views.xml',
        'views/precision_production_iot_menu.xml',
        'data/iot_device_data.xml',  # Sample device configurations
    ],
    'demo': [
        # Demo data could be added here if needed
    ],
    'assets': {
        'web.assets_backend': [
            'precision_production_iot/static/src/css/precision_iot_widgets.css',
            'precision_production_iot/static/src/js/precision_phase_kanban.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}