import re
with open('farm_isl/views/mrp_workcenter_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="costs_hour_second"[^>]*/>', '', content)
content = re.sub(r'<field name="costs_cycle_second"[^>]*/>', '', content)

with open('farm_isl/views/mrp_workcenter_isl_views.xml', 'w') as f:
    f.write(content)
