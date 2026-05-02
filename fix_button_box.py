import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            if '<xpath expr="//div[@name=\'button_box\']" position="inside">' in content:
                content = content.replace('<xpath expr="//div[@name=\'button_box\']" position="inside">', 
                    '<xpath expr="//sheet" position="inside">\n<div name="button_box" class="oe_button_box">')
                # Now we need to replace the next </xpath> with </div></xpath>
                # But this is risky if there are multiple.
            
                with open(path, 'w') as file:
                    file.write(content)
