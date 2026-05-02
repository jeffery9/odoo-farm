with open('farm_orchard_horticulture/models/orchard_operation.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == "_inherit = 'stock.lot'":
        continue
    if line.strip() == "_inherit = [":
        new_lines.append("    _inherit = [\n        'stock.lot',\n        'agri.biological.inventory.mixin',\n")
    else:
        new_lines.append(line)

with open('farm_orchard_horticulture/models/orchard_operation.py', 'w') as f:
    f.writelines(new_lines)
