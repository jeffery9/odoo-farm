# -*- coding: utf-8 -*-
{
    "name": "Industrial IoT (IIoT) Integration",
    "summary": "工业物联网集成模块，支持设备管理、遥测数据处理、指令下发和OTA固件升级",
    "description": """
Industrial IoT (IIoT) Integration
===============================

This module provides comprehensive Industrial IoT capabilities including:

- Device management and profiles
- MQTT-based telemetry data processing
- Command and control capabilities
- OTA firmware management
- Configuration download for devices
- Integration with business objects through declarative rules

The module follows the architecture of using HTTP webhooks to interface with MQTT brokers,
avoiding direct MQTT connections from Odoo for better reliability and maintainability.
    """,
    "version": "19.0.1.0.0",
    "category": "Manufacturing/Internet of Things",
    "author": \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    "website": \"http://www.geninit.cn\",
    "depends": [
        "base",
        "web",
        "mail",
        "maintenance",  # For equipment integration
        "stock",  # For inventory tracking if needed
        "mrp",  # For manufacturing integration
        "http_routing",  # For HTTP routing capabilities
    ],
    "data": [
        "security/iiot_security.xml",
        "security/ir.model.access.csv",
        "views/iiot_device_profile_views.xml",
        "views/iiot_telemetry_rule_views.xml",
        "views/iiot_device_views.xml",
        "views/iiot_firmware_views.xml",
        "views/iiot_update_views.xml",
        "views/menu.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 0,
    "currency": "USD",
    "license": "OPL-1",
}
