import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml') and ('data' in root or 'sequence' in f):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # If it has bare tags instead of fields
            if '<name>' in content and '</name>' in content and '<record ' in content:
                content = content.replace('<name>', '<field name="name">').replace('</name>', '</field>')
                content = content.replace('<code>', '<field name="code">').replace('</code>', '</field>')
                content = content.replace('<prefix>', '<field name="prefix">').replace('</prefix>', '</field>')
                content = content.replace('<padding>', '<field name="padding">').replace('</padding>', '</field>')
                content = content.replace('<company_id eval="False"/>', '<field name="company_id" eval="False"/>')
                with open(path, 'w') as file:
                    file.write(content)
