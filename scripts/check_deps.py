import os
import ast

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

modules = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, '__manifest__.py'))]
dep_graph = {m: [d for d in get_manifest_deps(m) if d in modules] for m in modules}

def find_cycle(graph):
    visited = set()
    path = []
    
    def visit(node):
        if node in path:
            print(f"Cycle detected: {' -> '.join(path[path.index(node):])} -> {node}")
            return True
        if node in visited:
            return False
        
        visited.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            if visit(neighbor):
                return True
        path.pop()
        return False

    for node in graph:
        if visit(node):
            return True
    return False

if not find_cycle(dep_graph):
    print("No circular dependencies detected between local modules.")

# Print summary of L2 inter-dependencies
print("\nChecking L2 Peer Dependencies (Forbidden):")
l2_modules = ['farm_crop', 'farm_livestock', 'farm_aquaculture', 'farm_apiculture', 'farm_mushroom', 'farm_orchard_horticulture', 'farm_viticulture']
for m in l2_modules:
    if m in dep_graph:
        peers = [d for d in dep_graph[m] if d in l2_modules and d != m]
        if peers:
            print(f"VIOLATION: {m} depends on peers: {peers}")
