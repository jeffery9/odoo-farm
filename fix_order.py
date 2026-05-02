import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    menus = re.findall(r'<menuitem[^>]*/>|<menuitem[^>]*>.*?</menuitem>', content, re.DOTALL)
    if not menus: return
    
    # Remove menus from original
    for m in menus:
        content = content.replace(m, '')
        
    # Put menus at the end
    content = content.replace('</odoo>', '') + '\n' + '\n'.join(menus) + '\n</odoo>'
    
    with open(path, 'w') as f:
        f.write(content)

fix_file('farm_multi_farm_base/views/entity_views.xml')
