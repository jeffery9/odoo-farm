import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Extract records and menuitems (the actual payload)
    payload = re.findall(r'<(record|menuitem|template|function|workflow|delete|act_window|report)[^>]*>.*?</\1>|<(menuitem|template|act_window|report|delete|function)[^/>]*/>', content, re.DOTALL)
    
    # Reconstruct the file with clean format
    records = []
    # findall with groups returns tuples, we need to join them
    # Actually, re.findall with multiple groups is tricky. Let's use a simpler approach.
    
    # Remove all XML boilerplate
    content = re.sub(r'<\?xml[^?]*\?>', '', content)
    content = re.sub(r'<odoo[^>]*>', '', content)
    content = content.replace('</odoo>', '')
    content = re.sub(r'<data[^>]*>', '', content)
    content = content.replace('</data>', '')
    
    # Clean up whitespace and comments that might be causing "extra content" errors
    content = content.strip()
    
    new_content = '<?xml version="1.0" encoding="utf-8"?>\n<odoo>\n' + content + '\n</odoo>'
    
    with open(path, 'w') as f:
        f.write(new_content)

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml') and ('farm_financial' in root or 'farm_valuation' in root or 'farm_subsidy' in root or 'farm_biological' in root or 'farm_insurance' in root):
            fix_file(os.path.join(root, f))
