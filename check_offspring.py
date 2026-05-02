import re

with open('farm_livestock/models/farm_lot.py', 'r') as f:
    content = f.read()
    
# check if mother_id or dam_id exists
if 'mother_id' in content:
    print("mother_id exists")
if 'dam_id' in content:
    print("dam_id exists")
