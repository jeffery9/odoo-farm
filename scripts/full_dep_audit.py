import os
import ast
from pprint import pprint

def get_manifest_deps(path):
    manifest_path = os.path.join(path, '__manifest__.py')
    if not os.path.exists(manifest_path):
        return []
    try:
        with open(manifest_path, 'r') as f:
            manifest_data = ast.literal_eval(f.read())
            return manifest_data.get('depends', [])
    except Exception:
        return []

modules = sorted([d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, '__manifest__.py'))])
dep_graph = {m: [d for d in get_manifest_deps(m) if d in modules] for m in modules}

# 1. Layer Definitions based on our recent refactoring
layer_0 = ['farm_core', 'agri_iot', 'farm_isl']
layer_1 = ['farm_operation', 'farm_supply', 'farm_iot', 'farm_multi_farm', 'farm_financial', 'farm_equipment', 'farm_hr', 'farm_marketing', 'farm_agri_science', 'farm_mrp', 'farm_ux']
layer_2_industry = ['farm_crop', 'farm_livestock', 'farm_aquaculture', 'farm_apiculture', 'farm_mushroom', 'farm_orchard_horticulture', 'farm_viticulture']
layer_2_functional = [m for m in modules if m not in layer_0 + layer_1 + layer_2_industry and not m.startswith('farm_ai')]
layer_3 = [m for m in modules if m.startswith('farm_ai')]

def get_layer(mod):
    if mod in layer_0: return 0
    if mod in layer_1: return 1
    if mod in layer_2_industry: return 2
    if mod in layer_2_functional: return 2
    if mod in layer_3: return 3
    return 99

print("=== ARCHITECTURAL DEPENDENCY AUDIT ===\n")

violations = []

# 2. Check for Upward Dependencies (Lower layer depending on higher layer)
for mod, deps in dep_graph.items():
    mod_layer = get_layer(mod)
    for dep in deps:
        dep_layer = get_layer(dep)
        if mod_layer < dep_layer:
            violations.append(f"[UPWARD DEPENDENCY] L{mod_layer} '{mod}' depends on L{dep_layer} '{dep}'")

# 3. Check for Cross-Industry Dependencies (L2 Industry apps depending on each other)
for mod in layer_2_industry:
    if mod in dep_graph:
        for dep in dep_graph[mod]:
            if dep in layer_2_industry and dep != mod:
                violations.append(f"[PEER VIOLATION] L2 Industry '{mod}' depends on Peer L2 Industry '{dep}'")

# 4. Find Circular Dependencies
def find_cycle(graph):
    visited = set()
    path = []
    
    def visit(node):
        if node in path:
            cycle = path[path.index(node):] + [node]
            return cycle
        if node in visited:
            return None
        
        visited.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            cycle = visit(neighbor)
            if cycle: return cycle
        path.pop()
        return None

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return None

cycle = find_cycle(dep_graph)
if cycle:
    violations.append(f"[FATAL: CIRCULAR DEPENDENCY] {' -> '.join(cycle)}")

if violations:
    print("❌ VIOLATIONS FOUND:")
    for v in violations:
        print(f"  - {v}")
else:
    print("✅ PERFECT ARCHITECTURE: No layer violations, peer dependencies, or circular dependencies found.")

# 5. Print Orphan Modules (No internal dependencies)
orphans = [m for m, deps in dep_graph.items() if not deps and m != 'farm_core' and m != 'agri_iot']
if orphans:
    print(f"\n⚠️ WARNING: Found modules with NO internal dependencies (are they disconnected?):")
    for o in orphans:
        print(f"  - {o}")

