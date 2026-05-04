import re
with open('farm_processing/views/mrp_production_pivot_view.xml', 'r') as f:
    content = f.read()

# Only keep product_qty which exists in mrp.production
content = re.sub(r'<field name="scrap_qty"[^>]*/>', '', content)
content = re.sub(r'<field name="loss_rate"[^>]*/>', '', content)
content = re.sub(r'<field name="total_energy_cost"[^>]*/>', '', content)

with open('farm_processing/views/mrp_production_pivot_view.xml', 'w') as f:
    f.write(content)
