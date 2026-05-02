import os
import ast

modules = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, '__manifest__.py'))]

for m in modules:
    man = os.path.join(m, '__manifest__.py')
    with open(man, 'r') as f:
        try:
            data = ast.literal_eval(f.read())
            deps = data.get('depends', [])
            for d in deps:
                if d not in modules and d not in ['base', 'mail', 'product', 'stock', 'project', 'account', 'purchase', 'sale', 'hr', 'mrp', 'website', 'loyalty', 'web', 'board', 'hr_timesheet', 'maintenance', 'quality_control', 'base_geolocalize', 'fleet', 'base_setup', 'pos_sale', 'point_of_sale']:
                    print(f"Module {m} depends on {d} which might not exist")
        except Exception as e:
            pass
