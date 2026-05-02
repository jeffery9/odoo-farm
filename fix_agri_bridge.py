with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

# 1. header -> sheet before
def repl_header(m):
    inner = m.group(1)
    return '<xpath expr="//sheet" position="before">\n<header>\n' + inner + '\n</header>\n</xpath>'
import re
content = re.sub(r'<xpath expr="//header" position="inside">(.*?)</xpath>', repl_header, content, flags=re.DOTALL)

# 2. Fix the buttons in header
content = content.replace('name="action_update_yield_estimate"', 'name="action_update_yield_estimate_btn"')
content = content.replace('name="action_apply_agri_intervention"', 'name="action_apply_agri_intervention_btn"')

# 3. Fix button_box since mrp_production doesn't have it natively in Odoo 19
def repl_box(m):
    inner = m.group(1)
    return '<xpath expr="//sheet" position="inside">\n<div name="button_box" class="oe_button_box">\n' + inner + '\n</div>\n</xpath>'
content = re.sub(r'<xpath expr="//div\[@name=\'button_box\'\]" position="inside">(.*?)</xpath>', repl_box, content, flags=re.DOTALL)

with open('agri_precision_core/views/precision_bridge_views.xml', 'w') as f:
    f.write(content)
