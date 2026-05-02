import re
with open('farm_iot/__manifest__.py', 'r') as f:
    content = f.read()

content = content.replace('views/farm_automation_rules_views.xml', 'views/farm_automation_views.xml')

with open('farm_iot/__manifest__.py', 'w') as f:
    f.write(content)
