import re

with open('farm_apiculture/models/apiculture_operation.py', 'r') as f:
    content = f.read()

# Add missing fields to farm.lot.hive
add_hive = """    honey_production_rate = fields.Float("Honey Production Rate")
"""
content = content.replace('    honey_store_level = fields.Float("Honey Store Level")', add_hive + '    honey_store_level = fields.Float("Honey Store Level")')

add_insp = """    honey_production_rate = fields.Float(related="hive_id.honey_production_rate", readonly=False)
"""
content = content.replace('    honey_store_level = fields.Float(related="hive_id.honey_store_level", readonly=False)', add_insp + '    honey_store_level = fields.Float(related="hive_id.honey_store_level", readonly=False)')

with open('farm_apiculture/models/apiculture_operation.py', 'w') as f:
    f.write(content)

