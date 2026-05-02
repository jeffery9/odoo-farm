with open('farm_operation/models/agri_intervention_mixin.py', 'r') as f:
    content = f.read()

content = content.replace("domain=\"[('is_drone', '=', True)]\"", "")

with open('farm_operation/models/agri_intervention_mixin.py', 'w') as f:
    f.write(content)
