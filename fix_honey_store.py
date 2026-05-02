import re

with open('farm_apiculture/models/apiculture_operation.py', 'r') as f:
    content = f.read()

# Add missing fields to farm.lot.hive
add_hive = """    honey_store_level = fields.Float("Honey Store Level")
"""
content = content.replace('    hive_location = fields.Char("Location")', add_hive + '    hive_location = fields.Char("Location")')

add_insp = """    honey_store_level = fields.Float(related="hive_id.honey_store_level", readonly=False)
"""
content = content.replace('    hive_location = fields.Char(related="hive_id.hive_location", readonly=False)', add_insp + '    hive_location = fields.Char(related="hive_id.hive_location", readonly=False)')

with open('farm_apiculture/models/apiculture_operation.py', 'w') as f:
    f.write(content)

