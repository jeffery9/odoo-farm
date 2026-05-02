import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            if 'js_class' in content or 'widget=' in content:
                # check if it's commented out in manifest
                module_dir = os.path.dirname(os.path.dirname(path)) if 'views/' in path else os.path.dirname(path)
                manifest_path = os.path.join(module_dir, '__manifest__.py')
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r') as mf:
                        m_content = mf.read()
                    
                    view_rel_path = path[len(module_dir)+1:]
                    if f"# '{view_rel_path}'" in m_content or f'# "{view_rel_path}"' in m_content:
                        print(f"Found OWL/JS widget in commented out view: {path}")

