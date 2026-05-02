import re

with open('precision_production/__manifest__.py', 'r') as f:
    content = f.read()

content = content.replace('"views/wizard_views.xml",\n        "views/phase_execution_views.xml",', '"views/phase_execution_views.xml",\n        "views/wizard_views.xml",')

with open('precision_production/__manifest__.py', 'w') as f:
    f.write(content)
