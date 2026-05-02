import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            c2 = re.sub(r' attrs="[^"]*"', '', content)
            c2 = re.sub(r' states="[^"]*"', '', c2)
            c2 = re.sub(r' expand="[^"]*"', '', c2)
            
            if c2 != content:
                with open(path, 'w') as file:
                    file.write(c2)
