import re
with open('farm_processing/views/mrp_bom_views.xml', 'r') as f:
    content = f.read()

content = content.replace('/tree/', '/list/')

with open('farm_processing/views/mrp_bom_views.xml', 'w') as f:
    f.write(content)
