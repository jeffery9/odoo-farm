import os
with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as file:
    content = file.read()

content = content.replace('\\n', '\n')
with open('agri_precision_core/views/precision_bridge_views.xml', 'w') as file:
    file.write(content)
