import os
import re

def normalize_xml_v5(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract real content (records, menuitems, etc.)
    # Remove xml decl, odoo, data tags
    content = re.sub(r'<\?xml.*?\?>', '', content)
    content = re.sub(r'<\/?odoo[^>]*?>', '', content)
    content = re.sub(r'<\/?data[^>]*?>', '', content)
    content = content.strip()
    
    if not content: return
    
    # Final structure: xml decl -> odoo -> data -> content
    new_content = '<?xml version="1.0" encoding="utf-8"?>\n<odoo>\n<data>\n' + content + '\n</data>\n</odoo>\n'
    
    with open(file_path, 'w') as f:
        f.write(new_content)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.xml') and ('farm_' in root or 'agri_' in root) and 'static' not in root:
            normalize_xml_v5(os.path.join(root, file))
