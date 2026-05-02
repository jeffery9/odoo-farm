import re

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="total_cumulative_yield"[^>]*/>', '<!-- field total_cumulative_yield removed -->', content)
content = re.sub(r'<field name="last_harvest_yield"[^>]*/>', '<!-- field last_harvest_yield removed -->', content)
content = re.sub(r'<field name="last_harvest_date"[^>]*/>', '<!-- field last_harvest_date removed -->', content)

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'w') as f:
    f.write(content)
