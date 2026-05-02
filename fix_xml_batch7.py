import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Extract records and menuitems
    content = re.sub(r'<\?xml[^?]*\?>', '', content)
    content = re.sub(r'<odoo[^>]*>', '', content)
    content = content.replace('</odoo>', '')
    content = re.sub(r'<data[^>]*>', '', content)
    content = content.replace('</data>', '')
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Fix old Odoo < 17 attributes
    content = re.sub(r' attrs="[^"]*"', '', content)
    content = re.sub(r' states="[^"]*"', '', content)
    content = re.sub(r' expand="[^"]*"', '', content)

    content = content.strip()
    new_content = '<?xml version="1.0" encoding="utf-8"?>\n<odoo>\n' + content + '\n</odoo>'
    
    with open(path, 'w') as f:
        f.write(new_content)

batch7 = ["farm_crop", "farm_viticulture", "farm_winery", "farm_apiculture", "farm_mushroom", "farm_floriculture", "farm_orchard_horticulture", "farm_medicinal_plants", "farm_seed_industry", "farm_fermentation", "farm_greenhouse", "precision_production", "precision_production_iot", "agri_precision_core", "farm_robotics", "farm_green_monitor", "farm_isl", "farm_dashboard", "farm_data_security", "farm_ai_llm_integration"]

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            if any(m in root for m in batch7):
                fix_file(os.path.join(root, f))
