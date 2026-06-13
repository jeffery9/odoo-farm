import os
import re

def normalize_xml(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove all odoo/data tags to start clean
    content = re.sub(r'<\/?odoo>', '', content)
    content = re.sub(r'<\/?data>', '', content)
    content = content.strip()
    
    # Wrap in odoo/data
    new_content = '<?xml version="1.0" encoding="utf-8"?>\n<odoo>\n<data>\n' + content + '\n</data>\n</odoo>\n'
    
    # Ensure only one xml decl
    if new_content.count('<?xml') > 1:
         new_content = re.sub(r'<\?xml.*?\?>\s*', '', new_content, count=1)
         # but wait, I just added one. 
         # Let's just fix it properly.
    
    lines = new_content.splitlines()
    final_lines = []
    has_decl = False
    for line in lines:
        if line.startswith('<?xml'):
            if not has_decl:
                final_lines.append(line)
                has_decl = True
        else:
            final_lines.append(line)
            
    with open(file_path, 'w') as f:
        f.write('\n'.join(final_lines) + '\n')

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.xml') and ('farm_' in root or 'agri_' in root) and 'static' not in root:
            normalize_xml(os.path.join(root, file))
