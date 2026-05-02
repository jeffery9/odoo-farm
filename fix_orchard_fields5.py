import re

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'r') as f:
    content = f.read()

# Remove the whole yield_record_ids field including its children
content = re.sub(r'<field name="yield_record_ids">.*?</field>', '<!-- field yield_record_ids removed -->', content, flags=re.DOTALL)
content = re.sub(r'<field name="maintenance_log_ids">.*?</field>', '<!-- field maintenance_log_ids removed -->', content, flags=re.DOTALL)
content = re.sub(r'<field name="yield_history"[^>]*/>', '', content)

with open('farm_orchard_horticulture/views/fruit_tree_views.xml', 'w') as f:
    f.write(content)
