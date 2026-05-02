import re
with open('farm_iot/__manifest__.py', 'r') as f:
    content = f.read()

content = re.sub(r'\'views/storage_env_views.xml\',', '', content)

with open('farm_iot/__manifest__.py', 'w') as f:
    f.write(content)
