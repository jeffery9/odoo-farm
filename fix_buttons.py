import re

with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

# Replace action_update_yield_estimate and action_apply_agri_intervention
# which have parameters in mrp.production (Odoo 19 buttons cannot call functions with params without context mapping, but they complained anyway)
content = content.replace('name="action_update_yield_estimate"', 'name="action_update_yield_estimate_btn"')
content = content.replace('name="action_apply_agri_intervention"', 'name="action_apply_agri_intervention_btn"')

with open('agri_precision_core/views/precision_bridge_views.xml', 'w') as f:
    f.write(content)
