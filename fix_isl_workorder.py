import re
with open('farm_isl/views/mrp_workorder_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<page string="Operations">.*?</page>', '', content, flags=re.DOTALL)

with open('farm_isl/views/mrp_workorder_isl_views.xml', 'w') as f:
    f.write(content)
