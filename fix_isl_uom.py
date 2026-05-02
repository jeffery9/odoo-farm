import re
with open('farm_isl/views/sale_order_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="product_uom"[^>]*/>', '<field name="product_uom_id"/>', content)

with open('farm_isl/views/sale_order_isl_views.xml', 'w') as f:
    f.write(content)
