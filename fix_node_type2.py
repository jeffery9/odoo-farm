with open('farm_supply_analytics/models/supply_chain_analytics.py', 'r') as f:
    content = f.read()

content = content.replace("('distributor', 'Distributor/Customer')\n    ])", "('distributor', 'Distributor/Customer')\n    ], ondelete={'supplier': 'set default', 'farm': 'set default', 'processing': 'set default', 'warehouse': 'set default', 'distributor': 'set default'})")
with open('farm_supply_analytics/models/supply_chain_analytics.py', 'w') as f:
    f.write(content)
