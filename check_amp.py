import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Find & not followed by a valid entity
            invalid_amps = re.findall(r'&(?!(?:amp|quot|apos|lt|gt|#\d+);)', content)
            if invalid_amps:
                print(f"Found {len(invalid_amps)} invalid ampersands in {path}")
