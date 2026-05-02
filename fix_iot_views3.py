import re
with open('farm_iot/views/iiot_device_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="operator_id"[^>]*/>', '', content)

with open('farm_iot/views/iiot_device_views.xml', 'w') as f:
    f.write(content)
