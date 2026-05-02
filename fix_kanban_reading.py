import re

with open('precision_production_iot/views/phase_execution_iot_views.xml', 'r') as f:
    content = f.read()

content = content.replace('invisible="not reading.deviation_percent"', 't-if="reading.deviation_percent"')

with open('precision_production_iot/views/phase_execution_iot_views.xml', 'w') as f:
    f.write(content)
