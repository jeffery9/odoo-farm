import re
with open('precision_production_iot/__manifest__.py', 'r') as f:
    content = f.read()

content = content.replace("'views/precision_production_iot_menu.xml',", "'views/phase_execution_iot_views.xml',\n        'views/precision_production_iot_menu.xml',")

with open('precision_production_iot/__manifest__.py', 'w') as f:
    f.write(content)
