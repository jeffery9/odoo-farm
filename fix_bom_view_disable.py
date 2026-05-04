import re
with open('farm_processing/views/mrp_bom_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<record id="view_mrp_bom_form_inherit_farm_v2"', '<!-- <record id="view_mrp_bom_form_inherit_farm_v2"')
content = content.replace('</record>', '</record> -->')

with open('farm_processing/views/mrp_bom_views.xml', 'w') as f:
    f.write(content)
