with open('farm_orchard_horticulture/models/orchard_operation.py', 'r') as f:
    content = f.read()

# Restore OrchardOperation _inherit
content = content.replace("    _inherit = [\n        'stock.lot',\n        'agri.biological.inventory.mixin',\n'mail.thread', 'mail.activity.mixin', 'agri.quality.gate.mixin']", "    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.quality.gate.mixin']")
# If it's a single line:
content = content.replace("_inherit = ['stock.lot', 'agri.biological.inventory.mixin', 'mail.thread', 'mail.activity.mixin', 'agri.quality.gate.mixin']", "_inherit = ['mail.thread', 'mail.activity.mixin', 'agri.quality.gate.mixin']")

with open('farm_orchard_horticulture/models/orchard_operation.py', 'w') as f:
    f.write(content)
