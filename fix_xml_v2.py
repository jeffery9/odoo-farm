import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Remove all <data> and </data> tags
    content = re.sub(r'<data[^>]*>', '', content)
    content = content.replace('</data>', '')
    
    # Remove existing <?xml...?> and <odoo>...</odoo>
    content = re.sub(r'<\?xml[^?]*\?>', '', content)
    content = content.replace('<odoo>', '').replace('</odoo>', '').strip()
    
    # Wrap in <?xml...?> and <odoo> (NO <data>)
    new_content = '<?xml version="1.0" encoding="utf-8"?>\n<odoo>\n' + content + '\n</odoo>'
    
    with open(path, 'w') as f:
        f.write(new_content)

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml') and ('farm_financial' in root or 'farm_valuation' in root or 'farm_subsidy' in root or 'farm_biological' in root or 'farm_insurance' in root):
            fix_file(os.path.join(root, f))
