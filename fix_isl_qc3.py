import re
with open('farm_isl/__manifest__.py', 'r') as f:
    content = f.read()

content = re.sub(r'"views/qc_isl_views\.xml",', '', content)

with open('farm_isl/__manifest__.py', 'w') as f:
    f.write(content)
