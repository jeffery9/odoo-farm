import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Find all multiline comments
            comments = re.findall(r'<!--(.*?)-->', content, flags=re.DOTALL)
            for c in comments:
                if '<record' in c:
                    print(f"Found commented out record in {path}")
