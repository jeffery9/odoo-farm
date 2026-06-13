import os
import re

def normalize_xml(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove all odoo/data tags and xml decl to start clean
    content = re.sub(r'<\?xml.*?\?>', '', content)
    content = re.sub(r'<\/?odoo>', '', content)
    content = re.sub(r'<\/?data>', '', content)
    content = content.strip()
    
    # Wrap ONLY in data (standard Odoo 17+ pattern)
    new_content = '<?xml version="1.0" encoding="utf-8"?>\n<data>\n' + content + '\n</data>\n'
    
    with open(file_path, 'w') as f:
        f.write(new_content)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.xml') and ('farm_' in root or 'agri_' in root) and 'static' not in root:
            normalize_xml(os.path.join(root, file))
