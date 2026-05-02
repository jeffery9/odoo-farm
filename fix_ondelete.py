import re

with open('farm_multi_farm_base/models/internal_settlement.py', 'r') as f:
    content = f.read()

content = content.replace("], string='Type', default='general', required=True)", "], string='Type', default='general', required=True, ondelete={'general': 'set default'})")
with open('farm_multi_farm_base/models/internal_settlement.py', 'w') as f:
    f.write(content)

with open('farm_multi_farm_base/models/extension_models.py', 'r') as f:
    content = f.read()

content = content.replace("], ondelete={'resource_rental': 'set default'})", "]")
content = content.replace("])", "], ondelete={'resource_rental': 'set default', 'service_fee': 'set default', 'joint_procurement': 'set default', 'marketing_fee': 'set default', 'management_fee': 'set default'})")
with open('farm_multi_farm_base/models/extension_models.py', 'w') as f:
    f.write(content)
