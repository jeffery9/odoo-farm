import re

with open('farm_apiculture/models/apiculture_operation.py', 'r') as f:
    content = f.read()

# Add missing fields to farm.lot.hive
add_hive = """    hive_location = fields.Char("Location")
    colony_population = fields.Integer("Population")
    bee_species = fields.Char("Species")
    bee_breed = fields.Char("Breed")"""
content = content.replace("    queen_age_months = fields.Integer(\"Queen Age (Months)\")", add_hive + '\n    queen_age_months = fields.Integer("Queen Age (Months)")')

# Add missing fields to farm.hive.inspection as related
add_insp = """    hive_location = fields.Char(related="hive_id.hive_location", readonly=False)
    colony_strength = fields.Selection(related="hive_id.colony_strength", readonly=False)
    colony_population = fields.Integer(related="hive_id.colony_population", readonly=False)
    queen_status = fields.Selection(related="hive_id.queen_status", readonly=False)
    queen_age_months = fields.Integer(related="hive_id.queen_age_months", readonly=False)
    bee_species = fields.Char(related="hive_id.bee_species", readonly=False)
    bee_breed = fields.Char(related="hive_id.bee_breed", readonly=False)
    nectar_sources = fields.Char("Nectar Sources")
    flowering_plants = fields.Char("Flowering Plants")
    nectar_availability = fields.Selection([('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], "Nectar Availability", default='medium')
    honey_production_stage = fields.Selection([('nectar', 'Nectar Flow'), ('capping', 'Capping'), ('ready', 'Ready for Harvest')], "Production Stage", default='nectar')
    expected_yield_volume = fields.Float("Expected Yield")
    last_harvest_date = fields.Date("Last Harvest")
    weather_condition = fields.Char("Weather Condition")
    temperature = fields.Float("Temperature")
    humidity = fields.Float("Humidity")
    pest_disease_status = fields.Char("Pest/Disease Status")
    treatment_applied = fields.Char("Treatment Applied")
    treatment_date = fields.Date("Treatment Date")
"""
content = content.replace('    hive_id = fields.Many2one(\'farm.lot.hive\', string="Hive to Inspect")', '    hive_id = fields.Many2one(\'farm.lot.hive\', string="Hive to Inspect")\n' + add_insp)

with open('farm_apiculture/models/apiculture_operation.py', 'w') as f:
    f.write(content)

with open('farm_apiculture/views/apiculture_operation_views.xml', 'r') as f:
    xml = f.read()

xml = xml.replace('<field name="model">farm.apiculture.operation</field>', '<field name="model">farm.hive.inspection</field>')
xml = xml.replace('id="view_farm_apiculture_operation_form"', 'id="view_farm_hive_inspection_form"')

with open('farm_apiculture/views/apiculture_operation_views.xml', 'w') as f:
    f.write(xml)
