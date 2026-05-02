import re
with open('farm_isl/views/product_template_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="uom_po_id"[^>]*/>', '', content)
content = re.sub(r'<field name="uom_id"[^>]*/>', '', content)
content = re.sub(r'<field name="tracking"[^>]*/>', '', content)

with open('farm_isl/views/product_template_isl_views.xml', 'w') as f:
    f.write(content)
