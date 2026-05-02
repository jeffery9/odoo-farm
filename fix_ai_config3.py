import re
with open('farm_ai_core/views/ai_config_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="requests_per_minute"[^>]*/>', '', content)
content = re.sub(r'<field name="requests_per_day"[^>]*/>', '', content)

with open('farm_ai_core/views/ai_config_views.xml', 'w') as f:
    f.write(content)
