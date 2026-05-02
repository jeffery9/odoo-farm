import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Remove all <data> and </data> tags (ignoring attributes like noupdate)
    content = re.sub(r'<data[^>]*>', '', content)
    content = content.replace('</data>', '')
    
    # Ensure it starts with <?xml...?> <odoo> <data> and ends with </data> </odoo>
    # This is the safest format for Odoo 19
    content = re.sub(r'<\?xml[^?]*\?>', '', content)
    content = content.replace('<odoo>', '').replace('</odoo>', '').strip()
    
    new_content = '<?xml version="1.0" encoding="utf-8"?>\n<odoo>\n<data>\n' + content + '\n</data>\n</odoo>'
    
    with open(path, 'w') as f:
        f.write(new_content)

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml') and ('farm_financial' in root or 'farm_valuation' in root or 'farm_subsidy' in root or 'farm_biological' in root or 'farm_insurance' in root):
            fix_file(os.path.join(root, f))
