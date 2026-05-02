import re

with open('farm_apiculture/models/apiculture_operation.py', 'r') as f:
    content = f.read()

add_hive = """    migration_schedule = fields.Char("Migration Schedule")
"""
content = content.replace('    last_harvest_yield = fields.Float("Last Harvest Yield")', add_hive + '    last_harvest_yield = fields.Float("Last Harvest Yield")')

add_insp = """    migration_schedule = fields.Char(related="hive_id.migration_schedule", readonly=False)
"""
content = content.replace('    last_harvest_yield = fields.Float(related="hive_id.last_harvest_yield", readonly=False)', add_insp + '    last_harvest_yield = fields.Float(related="hive_id.last_harvest_yield", readonly=False)')

with open('farm_apiculture/models/apiculture_operation.py', 'w') as f:
    f.write(content)

