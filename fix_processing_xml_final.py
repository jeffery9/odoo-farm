import re
with open('farm_processing/views/farm_processing_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="parent_lot_id"[^>]*/>', '<field name="parent_lot_ids" widget="many2many_tags"/>', content)
content = re.sub(r'parent="farm_operation\.menu_agri_campaign"', 'parent="farm_operation.menu_agricultural_campaigns"', content)

with open('farm_processing/views/farm_processing_views.xml', 'w') as f:
    f.write(content)
