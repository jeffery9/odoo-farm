import re
import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f == 'menu.xml':
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
                
            records = re.findall(r'<record[^>]*>.*?</record>', content, re.DOTALL)
            if records:
                # Remove records from content
                for r in records:
                    content = content.replace(r, '')
                
                # Insert records right after <odoo>
                content = content.replace('<odoo>', '<odoo>\n' + '\n'.join(records) + '\n')
                
                with open(path, 'w') as file:
                    file.write(content)
