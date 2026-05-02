import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Make sure <record> contains only <field> tags and no bare elements.
            # E.g. <list>, <form> directly under <record> is bad.
            # But they should be inside <field name="arch" type="xml">
            pass
