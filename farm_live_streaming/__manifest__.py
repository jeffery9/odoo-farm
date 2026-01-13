{
    'name': 'Farm Live Streaming & Douyin Integration',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Live Streaming and Douyin Platform Integration',
    'description': """
        Live streaming and Douyin integration module for Odoo 19 Farm Management System.
        - Douyin account authorization and binding [US-21-01]
        - Product synchronization with Douyin shop window [US-21-02]
        - Live room product association with traceability info [US-21-03]
        - Order auto-sync from Douyin to farm system [US-21-04]
        - Live streaming data statistics and analysis [US-21-05]
        - Live preview and promotion [US-21-06]
        - Live content archiving and reuse [US-21-07]
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['farm_marketing', 'farm_supply', 'sale', 'stock', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/douyin_api_data.xml',
        'data/douyin_cron_data.xml',
        'views/douyin_account_views.xml',
        'views/douyin_qualification_views.xml',
        'views/live_streaming_views.xml',
        'views/product_sync_views.xml',
        'views/live_order_views.xml',
        'views/live_statistics_views.xml',
        'views/live_promotion_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}