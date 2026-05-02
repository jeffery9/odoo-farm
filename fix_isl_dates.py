import re
with open('farm_isl/views/mrp_production_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="date_planned_start"[^>]*/>', '', content)
content = re.sub(r'<field name="date_planned_finished"[^>]*/>', '', content)

with open('farm_isl/views/mrp_production_isl_views.xml', 'w') as f:
    f.write(content)
