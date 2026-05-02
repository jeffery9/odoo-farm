import re
with open('farm_isl/views/stock_lot_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<button name="toggle_active"[^>]*>[\s\S]*?</button>', '', content)
content = re.sub(r'<field name="active"[^>]*/>', '', content)

with open('farm_isl/views/stock_lot_isl_views.xml', 'w') as f:
    f.write(content)
