import re
with open('farm_quality/views/quality_check_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<button name="action_open_quality_alert"[^>]*/>', '', content)

with open('farm_quality/views/quality_check_views.xml', 'w') as f:
    f.write(content)
