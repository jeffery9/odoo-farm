import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('_views.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Find all views that have inherit_id but their model is not the parent's model.
            # It's hard to dynamically guess. But I know farm.mushroom.operation, farm.medicinal.production, etc.
            # Let's just remove inherit_id and <xpath> wrapping, and put them inside <form><sheet>
            
            # Specifically for farm_mushroom and farm_medicinal_plants
            if 'farm_mushroom' in root or 'farm_medicinal_plants' in root or 'farm_apiculture' in root:
                # Replace <field name="inherit_id".../> with nothing
                # and <xpath ...> with <form><sheet>
                if 'inherit_id' in content and 'ref="mrp.' in content:
                    content = re.sub(r'<field name="inherit_id"[^>]*/>', '', content)
                    content = re.sub(r'<xpath[^>]*>', '<form><sheet>', content)
                    content = re.sub(r'</xpath>', '</sheet></form>', content)
                    
                    with open(path, 'w') as file:
                        file.write(content)
