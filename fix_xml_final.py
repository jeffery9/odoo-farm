import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Remove all XML boilerplate
    content = re.sub(r'<\?xml[^?]*\?>', '', content)
    content = re.sub(r'<odoo[^>]*>', '', content)
    content = content.replace('</odoo>', '')
    content = re.sub(r'<data[^>]*>', '', content)
    content = content.replace('</data>', '')
    
    # Remove all comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Clean up whitespace
    content = content.strip()
    
    # Reconstruct with ZERO whitespace after <odoo>
    new_content = '<?xml version="1.0" encoding="utf-8"?>\n<odoo>' + content + '</odoo>'
    
    with open(path, 'w') as f:
        f.write(new_content)

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml') and ('farm_financial' in root or 'farm_valuation' in root or 'farm_subsidy' in root or 'farm_biological' in root or 'farm_insurance' in root):
            fix_file(os.path.join(root, f))
