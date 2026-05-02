import os
import ast

def get_manifest_deps(module_path):
    manifest_path = os.path.join(module_path, '__manifest__.py')
    if not os.path.exists(manifest_path):
        return []
    with open(manifest_path, 'r') as f:
        try:
            manifest_data = ast.literal_eval(f.read())
            return manifest_data.get('depends', [])
        except Exception:
            return []

modules = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, '__manifest__.py'))]
graph = {m: get_manifest_deps(m) for m in modules}

def find_cycle(v, visited, stack, path):
    visited.add(v)
    stack.add(v)
    path.append(v)
    
    for neighbor in graph.get(v, []):
        if neighbor in stack:
            # Cycle found
            cycle_path = path[path.index(neighbor):]
            return cycle_path + [neighbor]
        if neighbor not in visited:
            res = find_cycle(neighbor, visited, stack, path)
            if res:
                return res
                
    stack.remove(v)
    path.pop()
    return None

visited = set()
for m in modules:
    if m not in visited:
        cycle = find_cycle(m, visited, set(), [])
        if cycle:
            print("Cycle detected:", " -> ".join(cycle))
            break
else:
    print("No cycle detected in manifest dependencies.")
