with open('farm_multi_farm_base/security/ir.model.access.csv', 'r') as f:
    lines = f.readlines()

new_lines = [lines[0]]
valid_models = ['cooperative_entity', 'farm_entity', 'resource_sharing', 'internal_settlement', 'franchise_farm', 'cooperative_member', 'agri_service', 'service_order', 'contract_farming_agreement', 'contract_farming_input_prepayment', 'contract_farming_yield_commitment', 'contract_farming_settlement']
for line in lines[1:]:
    model_name = line.split(',')[1].replace('.user', '')
    if model_name.replace('.', '_') in valid_models or model_name in valid_models or model_name == 'farm.regional.oversight':
        new_lines.append(line)

with open('farm_multi_farm_base/security/ir.model.access.csv', 'w') as f:
    f.writelines(new_lines)
