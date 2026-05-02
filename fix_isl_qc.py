import re
with open('farm_isl/views/qc_isl_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<field [^>]*/>', '', content)
content = re.sub(r'<field [^>]*>[\s\S]*?</field>', '', content)

with open('farm_isl/views/qc_isl_views.xml', 'w') as f:
    f.write(content)
