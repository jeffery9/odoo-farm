import os

def clean_xml(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if '<odoo>' in line or '</odoo>' in line:
            continue
        new_lines.append(line)
    
    with open(file_path, 'w') as f:
        f.writelines(new_lines)

for root, dirs, files in os.walk('farm_agritourism/views'):
    for file in files:
        if file.endswith('.xml'):
            clean_xml(os.path.join(root, file))
