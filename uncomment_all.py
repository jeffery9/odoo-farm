import os
import re

for root, dirs, files in os.walk('.'):
    if '__manifest__.py' in files:
        path = os.path.join(root, '__manifest__.py')
        with open(path, 'r') as f:
            content = f.read()
        
        # Uncomment # 'views/...'
        new_content = re.sub(r'#\s*(\'views/[^\']*?\',)', r'\1', content)
        new_content = re.sub(r'#\s*(\"views/[^\"]*?\",)', r'\1', new_content)
        
        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
