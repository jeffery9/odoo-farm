import re

files = [
    'farm_isl/views/sale_order_isl_views.xml',
    'farm_isl/views/purchase_order_isl_views.xml',
    'farm_isl/views/mrp_workorder_isl_views.xml',
]

for file in files:
    try:
        with open(file, 'r') as f:
            content = f.read()
        
        content = re.sub(r'<button name="action_confirm"[^>]*/>', '', content)
        content = re.sub(r'<button name="action_cancel"[^>]*/>', '', content)
        content = re.sub(r'<button name="button_confirm"[^>]*/>', '', content)
        content = re.sub(r'<button name="button_cancel"[^>]*/>', '', content)
        
        with open(file, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        pass
