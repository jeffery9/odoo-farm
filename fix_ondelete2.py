with open('farm_multi_farm_base/models/extension_models.py', 'r') as f:
    content = f.read()

content = content.replace("], ondelete={'resource_rental': 'set default', 'service_fee': 'set default', 'joint_procurement': 'set default', 'marketing_fee': 'set default', 'management_fee': 'set default'})", "], ondelete={'resource_rental': 'set default', 'service_fee': 'set default', 'joint_procurement': 'set default', 'marketing_fee': 'set default', 'management_fee': 'set default', 'profit_sharing': 'set default', 'internal_transaction': 'set default', 'subsidy_distribution': 'set default', 'netting_settlement': 'set default'})")

with open('farm_multi_farm_base/models/extension_models.py', 'w') as f:
    f.write(content)
