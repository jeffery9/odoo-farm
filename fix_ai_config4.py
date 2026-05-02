import re
with open('farm_ai_core/views/ai_config_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="temperature"[^>]*/>', '', content)
content = re.sub(r'<field name="max_tokens"[^>]*/>', '', content)

with open('farm_ai_core/views/ai_config_views.xml', 'w') as f:
    f.write(content)
