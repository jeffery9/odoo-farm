import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            content = re.sub(r'<inherit_id ref="([^"]+)"/>', r'<field name="inherit_id" ref="\1"/>', content)
            
            with open(path, 'w') as file:
                file.write(content)
