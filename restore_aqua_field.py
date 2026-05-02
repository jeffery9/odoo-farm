with open('farm_aquaculture/views/aquaculture_operation_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<!-- <field name="water_quality_status" invisible="1"/> -->', '<field name="water_quality_status" invisible="1"/>')

with open('farm_aquaculture/views/aquaculture_operation_views.xml', 'w') as f:
    f.write(content)
