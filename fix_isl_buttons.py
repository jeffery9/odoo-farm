import re
with open('farm_isl/views/mrp_production_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<button name="action_confirm"[^>]*/>', '', content)
content = re.sub(r'<button name="action_start"[^>]*/>', '', content)
content = re.sub(r'<button name="action_cancel"[^>]*/>', '', content)

with open('farm_isl/views/mrp_production_isl_views.xml', 'w') as f:
    f.write(content)
