import re

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="trunk_diameter"[^>]*/>', '<!-- field trunk_diameter removed -->', content)
content = re.sub(r'<field name="expected_harvest_date"[^>]*/>', '<!-- field expected_harvest_date removed -->', content)

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'w') as f:
    f.write(content)
