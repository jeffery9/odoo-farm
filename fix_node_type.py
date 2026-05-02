with open('farm_supply_core/models/agri_supply_chain_mixin.py', 'r') as f:
    content = f.read()

content = content.replace("], string='Node Type', required=True)", "], string='Node Type', required=True, default='producer', ondelete={'supplier': 'set default', 'producer': 'set default', 'processor': 'set default', 'distributor': 'set default', 'retailer': 'set default'})")
with open('farm_supply_core/models/agri_supply_chain_mixin.py', 'w') as f:
    f.write(content)
