import re
with open('farm_iot/views/iiot_device_views.xml', 'r') as f:
    content = f.read()

content = content.replace('industrial_iot.view_iiot_device_form', 'agri_iot.view_iiot_device_form')

with open('farm_iot/views/iiot_device_views.xml', 'w') as f:
    f.write(content)
