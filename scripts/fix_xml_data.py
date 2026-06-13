import os
import re

def fix_xml(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    if '<odoo>' in content and '<data>' not in content:
        # Simple wrap
        new_content = content.replace('<odoo>', '<odoo>\n    <data>')
        new_content = new_content.replace('</odoo>', '    </data>\n</odoo>')
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False

xml_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.xml') and ('farm_' in root or 'agri_' in root):
            xml_files.append(os.path.join(root, file))

count = 0
for f in xml_files:
    if fix_xml(f):
        count += 1

print(f"Fixed {count} XML files.")
