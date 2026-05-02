import re
with open('farm_quality/views/stock_lot_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<button name="action_reverse_traceability"[^>]*/>', '', content)

with open('farm_quality/views/stock_lot_views.xml', 'w') as f:
    f.write(content)
