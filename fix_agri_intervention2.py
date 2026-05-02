import re

with open('farm_operation/views/agri_intervention_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<xpath expr="//page\[@name=\'finished_steps\'\][^>]*>', '<!-- xpath removed -->', content)
content = re.sub(r'<field name="quality_grade" optional="show"/>\n\s*</xpath>', '<!-- field quality_grade removed -->', content)

with open('farm_operation/views/agri_intervention_views.xml', 'w') as f:
    f.write(content)
