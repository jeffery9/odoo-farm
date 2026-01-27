{
    "name": "Farm Crop Management",
    "version": "1.0",
    "category": "Industries/Agriculture",
    "summary": "Crop-specific management features: rotation history, variety management, and cultivation protocols",
    "description": """
        Crop-focused module that handles:
        - Crop rotation history and continuous cropping obstacles (US-01-09)
        - Crop-specific cultivation protocols
        - Variety management and tracking
    """,
    "author": "Odoo Farm Dev Team",
    "depends": [
        "farm_core",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/crop_rotation_history_views.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
}