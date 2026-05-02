import re
with open('farm_multi_farm_base/models/extension_models.py', 'r') as f:
    content = f.read()

# Wait, the search method was corrupted by my previous replace (which replaced all "])")
# I'll fix this manually.
