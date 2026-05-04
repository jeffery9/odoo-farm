import re
with open('farm_processing/views/mrp_bom_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<field name="processing_type" invisible="industry_type == \'standard\'"/>', '')

with open('farm_processing/views/mrp_bom_views.xml', 'w') as f:
    f.write(content)
