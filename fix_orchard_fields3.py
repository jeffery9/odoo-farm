import re

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="rootstock_variety"[^>]*/>', '<!-- field rootstock_variety removed -->', content)
content = re.sub(r'<field name="scion_variety"[^>]*/>', '<!-- field scion_variety removed -->', content)
content = re.sub(r'<field name="gdd_accumulated"[^>]*/>', '<!-- field gdd_accumulated removed -->', content)
content = re.sub(r'<field name="disease_status"[^>]*/>', '<!-- field disease_status removed -->', content)
content = re.sub(r'<field name="canopy_density"[^>]*/>', '<!-- field canopy_density removed -->', content)
content = re.sub(r'<field name="irrigation_status"[^>]*/>', '<!-- field irrigation_status removed -->', content)
content = re.sub(r'<field name="yield_history"[^>]*/>', '<!-- field yield_history removed -->', content)

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'w') as f:
    f.write(content)
