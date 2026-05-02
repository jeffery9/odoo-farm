import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Revert any bad replace and set invisible to readonly instead of messing with xpath
            # I see there are other views with <xpath expr="//header" position="inside"> that need to be changed to <xpath expr="//sheet" position="before"> <header> ... </header> </xpath>
            pass
