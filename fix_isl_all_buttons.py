import re
import os

for root, dirs, files in os.walk('farm_isl/views'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            content = re.sub(r'<button [^>]*/>', '', content)
            content = re.sub(r'<button [^>]*>[\s\S]*?</button>', '', content)
            
            with open(path, 'w') as file:
                file.write(content)

