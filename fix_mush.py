import re

def remove_missing(filename):
    with open(filename, 'r') as f:
        c = f.read()
    c = re.sub(r'<field name="[^"]*"\/>', '', c)
    with open(filename, 'w') as f:
        f.write(c)
        
# Wait, removing ALL fields makes the view useless. Let's see what fields are actually in farm.mushroom.production
