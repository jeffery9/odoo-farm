import re
with open('farm_operation/views/agri_intervention_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<button name="action_finalize_clearing"[^>]*/>', '', content)

with open('farm_operation/views/agri_intervention_views.xml', 'w') as f:
    f.write(content)
