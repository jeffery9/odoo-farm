import os
import ast

for root, dirs, files in os.walk('.'):
    if '__manifest__.py' in files and 'farm_multi_farm' in root:
        with open(os.path.join(root, '__manifest__.py'), 'r') as f:
            try:
                data = ast.literal_eval(f.read())
                for item in data.get('data', []):
                    if not os.path.exists(os.path.join(root, item)):
                        print(f"Missing {item} in {root}")
            except Exception as e:
                pass
