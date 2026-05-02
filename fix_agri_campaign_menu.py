import re
with open('farm_operation/views/agri_intervention_views.xml', 'r') as f:
    content = f.read()

content = content.replace('parent="menu_agri_campaign"', 'parent="menu_agricultural_campaigns"')

with open('farm_operation/views/agri_intervention_views.xml', 'w') as f:
    f.write(content)
