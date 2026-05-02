import re

files = [
    'precision_production/views/mrp_production_views.xml',
    'precision_production/views/mrp_workorder_views.xml',
    'precision_production/views/recipe_execution_dashboard.xml'
]

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # We just replaced <xpath expr="//header" position="inside"> with <xpath expr="//sheet" position="before">\n                <header>
    # The very next </xpath> should be closed with </header>
    parts = content.split('<xpath expr="//sheet" position="before">\n                <header>')
    if len(parts) > 1:
        new_content = parts[0]
        for part in parts[1:]:
            # Find the first </xpath> in this part and replace it
            subparts = part.split('</xpath>', 1)
            new_part = subparts[0] + '</header>\n            </xpath>' + subparts[1]
            new_content += '<xpath expr="//sheet" position="before">\n                <header>' + new_part
        with open(file, 'w') as f:
            f.write(new_content)
