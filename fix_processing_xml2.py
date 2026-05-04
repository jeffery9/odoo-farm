import re
with open('farm_processing/views/farm_processing_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<field name="parent_lot_id"/>', '<field name="parent_lot_ids" widget="many2many_tags"/>')

with open('farm_processing/views/farm_processing_views.xml', 'w') as f:
    f.write(content)
