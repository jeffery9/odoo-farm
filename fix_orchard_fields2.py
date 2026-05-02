import re

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="tree_age"[^>]*/>', '<!-- field tree_age removed -->', content)

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'w') as f:
    f.write(content)
