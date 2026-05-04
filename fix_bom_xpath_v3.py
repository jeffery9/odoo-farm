import re
with open('farm_processing/views/mrp_bom_views.xml', 'r') as f:
    content = f.read()

# Remove the problematic xpaths
content = re.sub(r'<xpath expr="//field\[@name=\'operation_ids\'\].*?</xpath>', '<!-- problematic xpath removed -->', content, flags=re.DOTALL)
content = re.sub(r'<xpath expr="//field\[@name=\'bom_line_ids\'\].*?</xpath>', '<!-- problematic xpath removed -->', content, flags=re.DOTALL)

with open('farm_processing/views/mrp_bom_views.xml', 'w') as f:
    f.write(content)
