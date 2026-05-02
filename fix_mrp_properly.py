import re

files = [
    'precision_production/views/mrp_production_views.xml',
    'precision_production/views/mrp_workorder_views.xml',
    'precision_production/views/recipe_execution_dashboard.xml',
    'precision_production/views/product_views.xml'
]

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # 1. First remove the old attrs/states stuff from these files to be safe
    content = re.sub(r' attrs="[^"]*"', '', content)
    content = re.sub(r' states="[^"]*"', '', content)
    content = re.sub(r' expand="[^"]*"', '', content)
    
    # 2. Fix the xpath for header. 
    # Find <xpath expr="//header" position="inside"> ... </xpath>
    # Change to <xpath expr="//header" position="inside"> ... </xpath> BUT wait, the problem was that <header> didn't exist in parent?
    # mrp.production form has a header. mrp.bom form doesn't have a header in Odoo 17/18?
    # Let's just change it to <xpath expr="//sheet" position="before"> <header> ... </header> </xpath>
    
    def repl(m):
        inner = m.group(1)
        return '<xpath expr="//sheet" position="before">\n<header>\n' + inner + '\n</header>\n</xpath>'
        
    content = re.sub(r'<xpath expr="//header" position="inside">(.*?)</xpath>', repl, content, flags=re.DOTALL)
    
    with open(file, 'w') as f:
        f.write(content)
