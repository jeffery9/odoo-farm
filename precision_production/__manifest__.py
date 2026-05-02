{
    "name": "Precision Production",
    "summary": "精密生产 - 参数/配方驱动的生产执行系统",
    "version": "19.0.1.0.0",
    "category": "Manufacturing",
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    "depends": [
        "base",
        "mail",
        "mrp",
        "stock",
        "farm_agri_science",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/mrp_production_views.xml",
        "views/mrp_workorder_views.xml",
        "views/stock_lot_views.xml",
        "views/phase_execution_views.xml",
        "views/wizard_views.xml",
        "views/recipe_execution_dashboard.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "precision_production/static/src/css/precision_execution_dashboard.css",
            "precision_production/static/src/js/precision_execution_dashboard.js",
        ],
    },
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
