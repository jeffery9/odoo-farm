import os
import ast

batch7 = ["farm_crop", "farm_viticulture", "farm_winery", "farm_apiculture", "farm_mushroom", "farm_floriculture", "farm_orchard_horticulture", "farm_medicinal_plants", "farm_seed_industry", "farm_fermentation", "farm_greenhouse", "precision_production", "precision_production_iot", "agri_precision_core", "farm_robotics", "farm_green_monitor", "farm_isl", "farm_dashboard", "farm_data_security", "farm_ai_llm_integration"]

for m in batch7:
    man = os.path.join(m, '__manifest__.py')
    if os.path.exists(man):
        with open(man, 'r') as f:
            try:
                data = ast.literal_eval(f.read())
                deps = data.get('depends', [])
                for d in deps:
                    if not os.path.exists(d) and d not in ['base', 'mail', 'product', 'stock', 'project', 'account', 'purchase', 'sale', 'hr', 'mrp', 'website', 'loyalty', 'web', 'board', 'hr_timesheet', 'maintenance', 'quality_control', 'base_geolocalize', 'fleet']:
                        print(f"Module {m} depends on {d} which might not exist")
            except Exception as e:
                pass
