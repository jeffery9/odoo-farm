import re
with open('farm_processing/views/mrp_bom_views.xml', 'r') as f:
    content = f.read()

content = content.replace("<xpath expr=\"//field[@name='operation_ids']/list/field[@name='workcenter_id']\"", "<xpath expr=\"//field[@name='operation_ids']//field[@name='workcenter_id']\"")
content = content.replace("<xpath expr=\"//field[@name='bom_line_ids']/list/field[@name='product_id']\"", "<xpath expr=\"//field[@name='bom_line_ids']//field[@name='product_id']\"")

with open('farm_processing/views/mrp_bom_views.xml', 'w') as f:
    f.write(content)
