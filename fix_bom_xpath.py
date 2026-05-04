import re
with open('farm_processing/views/mrp_bom_views.xml', 'r') as f:
    content = f.read()

content = content.replace("<xpath expr=\"//group[@name='main_group']\"", "<xpath expr=\"//sheet/group\"")

with open('farm_processing/views/mrp_bom_views.xml', 'w') as f:
    f.write(content)
