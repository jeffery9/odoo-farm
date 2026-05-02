import re

files = [
    'farm_livestock/views/updated_livestock_production_view.xml',
    'farm_aquaculture/views/updated_aquaculture_production_view.xml',
    'farm_mushroom/views/updated_mushroom_production_view.xml'
]

# We need to make sure the model is 'mrp.production' instead of 'farm...production' 
# or remove the inherit_id entirely so it loads.
for file in files:
    try:
        with open(file, 'r') as f:
            content = f.read()
        
        # Remove inherit_id
        content = re.sub(r'<field name="inherit_id"[^>]*/>', '', content)
        # Change to base form view
        content = re.sub(r'<notebook position="inside">', '<form><sheet><notebook>', content)
        content = re.sub(r'</notebook>', '</notebook></sheet></form>', content)
        
        with open(file, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        pass
