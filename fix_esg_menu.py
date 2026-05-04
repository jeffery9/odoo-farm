import os
import re

file_path = 'farm_esg/views/res_config_settings_views.xml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The error says farm_esg.esg_base_menu is missing.
# Let's see what menus are defined in farm_esg.
