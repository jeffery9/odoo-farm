import re

with open('farm_apiculture/models/apiculture_operation.py', 'r') as f:
    content = f.read()

add_hive = """    last_harvest_yield = fields.Float("Last Harvest Yield")
"""
content = content.replace('    honey_production_rate = fields.Float("Honey Production Rate")', add_hive + '    honey_production_rate = fields.Float("Honey Production Rate")')

add_insp = """    last_harvest_yield = fields.Float(related="hive_id.last_harvest_yield", readonly=False)
"""
content = content.replace('    honey_production_rate = fields.Float(related="hive_id.honey_production_rate", readonly=False)', add_insp + '    honey_production_rate = fields.Float(related="hive_id.honey_production_rate", readonly=False)')

with open('farm_apiculture/models/apiculture_operation.py', 'w') as f:
    f.write(content)

