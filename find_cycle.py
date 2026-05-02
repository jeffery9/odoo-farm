import os
import ast

deps = {}
for root, dirs, files in os.walk('.'):
    for f in files:
        if f == '__manifest__.py':
            path = os.path.join(root, f)
            module_name = os.path.basename(root)
            with open(path, 'r') as file:
                try:
                    data = ast.literal_eval(file.read())
                    deps[module_name] = data.get('depends', [])
                except Exception:
                    pass

def find_cycle(start, path):
    for neighbor in deps.get(start, []):
        if neighbor in path:
            cycle = path[path.index(neighbor):] + [neighbor]
            if len(cycle) > 2:  # Found real cycle
                return cycle
        else:
            c = find_cycle(neighbor, path + [neighbor])
            if c: return c
    return None

for mod in deps:
    c = find_cycle(mod, [mod])
    if c:
        print("CYCLE:", " -> ".join(c))
        break
