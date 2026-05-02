import re
with open('farm_isl/views/product_template_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="detailed_type"[^>]*/>', '', content)
content = re.sub(r'<field name="sale_ok"[^>]*/>', '', content)
content = re.sub(r'<field name="purchase_ok"[^>]*/>', '', content)

with open('farm_isl/views/product_template_isl_views.xml', 'w') as f:
    f.write(content)
