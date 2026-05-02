with open('farm_orchard_horticulture/models/orchard_operation.py', 'r') as f:
    content = f.read()

content = content.replace("    _inherit = ['stock.lot', 'agri.biological.inventory.mixin', \n        'agri.intervention.mixin',", "    _inherit = [\n        'agri.intervention.mixin',")

with open('farm_orchard_horticulture/models/orchard_operation.py', 'w') as f:
    f.write(content)
