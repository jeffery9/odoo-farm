import re
with open('farm_iot/views/digital_twin_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<button name="action_activate"[^>]*/>', '', content)

with open('farm_iot/views/digital_twin_views.xml', 'w') as f:
    f.write(content)
