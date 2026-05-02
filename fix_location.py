import re

with open('farm_apiculture/models/apiculture_operation.py', 'r') as f:
    content = f.read()

add_hive = """    current_location = fields.Char("Current Location")
"""
content = content.replace('    migration_schedule = fields.Char("Migration Schedule")', add_hive + '    migration_schedule = fields.Char("Migration Schedule")')

add_insp = """    current_location = fields.Char(related="hive_id.current_location", readonly=False)
"""
content = content.replace('    migration_schedule = fields.Char(related="hive_id.migration_schedule", readonly=False)', add_insp + '    migration_schedule = fields.Char(related="hive_id.migration_schedule", readonly=False)')

with open('farm_apiculture/models/apiculture_operation.py', 'w') as f:
    f.write(content)

