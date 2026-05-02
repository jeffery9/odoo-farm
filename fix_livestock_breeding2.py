import re
with open('farm_livestock/models/farm_lot.py', 'r') as f:
    content = f.read()

content = re.sub(r'# offspring_ids = fields\.One2many\([\s\S]*?#    \)', "offspring_ids = fields.One2many(\n        'stock.lot',\n        'breeding_record_id',\n        string='Offspring'\n    )", content)

with open('farm_livestock/models/farm_lot.py', 'w') as f:
    f.write(content)
