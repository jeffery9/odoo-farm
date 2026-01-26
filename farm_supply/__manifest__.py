{
    'name': 'Farm Supply & Inputs',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Input Management, Procurement and Compliance',
    'description': """
        Supply module for Odoo 19 Farm Management System.
        - Agricultural Input Catalog (Seeds, Fertilizers, Pesticides, Feed)
        - Purchase Order Integration with Safety Checks
        - Input Usage Forecasting and Stock Alerts
        - Dynamic Shelf-life Prediction based on IoT Temperature [US-09-07]
        - Post-harvest Pre-cooling Process Tracking [US-09-08]
        - Cold Storage Multi-zone and Humidity Management [US-09-09]
        - Quality-based Procurement Pricing [US-09-11]
        - Export Document Hub for Cross-border Trade [US-09-12]
        - Circular Asset Tracking for High-value Packaging [US-09-13]
        - VMI (Vendor Managed Inventory) Automation [US-09-14]
        - Joint Procurement for Cooperatives [US-09-15]
        - Supply Risk Radar Monitoring [US-09-16]
        - Safe POD (Proof of Delivery) with Temperature Control [US-09-17]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/seasonal_stock_views.xml',
        'views/supply_chain_management_views.xml',
        'views/supply_chain_vmi_views.xml',
        'views/temperature_management_views.xml',
        'views/cold_storage_views.xml',
        'views/vmi_procurement_views.xml',
        'views/delivery_tracking_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
