import re

with open('farm_aquaculture/views/aquaculture_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field name="[^"]*"\s*/>', '', content)
content = re.sub(r'<!--.*?-->', '', content)

with open('farm_aquaculture/views/aquaculture_isl_views.xml', 'w') as f:
    f.write(content)

