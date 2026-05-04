import re
with open('farm_processing/views/farm_processing_views.xml', 'r') as f:
    content = f.read()

content = content.replace('parent="farm_operation.menu_agri_campaign"', 'parent="farm_operation.menu_agricultural_campaigns"')

with open('farm_processing/views/farm_processing_views.xml', 'w') as f:
    f.write(content)
