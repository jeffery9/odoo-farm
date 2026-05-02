import re
import os

files = [
    'farm_isl/views/mrp_workcenter_isl_views.xml',
    'farm_isl/views/stock_picking_isl_views.xml',
    'farm_isl/views/purchase_order_isl_views.xml',
    'farm_isl/views/sale_order_isl_views.xml',
    'farm_isl/views/mrp_workorder_isl_views.xml',
    'farm_isl/views/stock_lot_isl_views.xml',
]

fields_to_remove = [
    'costs_hour', 'costs_cycle', 'date_deadline', 'date_planned'
]

for file in files:
    try:
        with open(file, 'r') as f:
            content = f.read()
        
        for field in fields_to_remove:
            content = re.sub(f'<field name="{field}"[^>]*/>', '', content)
            
        with open(file, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        pass
