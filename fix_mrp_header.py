import re

files = [
    'precision_production/views/mrp_production_views.xml',
    'precision_production/views/mrp_workorder_views.xml',
    'precision_production/views/recipe_execution_dashboard.xml'
]

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # It seems there is an extra </header> before </xpath>
    content = content.replace('</header>\n            </header>\n            </xpath>', '</header>\n            </xpath>')
    content = content.replace('</header>\n            </xpath>', '</header>\n            </xpath>') # Just ensuring
    
    with open(file, 'w') as f:
        f.write(content)
