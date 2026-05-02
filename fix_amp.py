import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Replace & with &amp; ONLY if it's not already an entity
            new_content = re.sub(r'&(?!(?:amp|quot|apos|lt|gt|#\d+|#x[a-fA-F0-9]+);)', '&amp;', content)
            
            if new_content != content:
                with open(path, 'w') as file:
                    file.write(new_content)
