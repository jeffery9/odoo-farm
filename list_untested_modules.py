import os

modules = []
for d in os.listdir('.'):
    if os.path.isdir(d) and (d.startswith('farm_') or d.startswith('agri_') or d.startswith('precision_')):
        if os.path.exists(os.path.join(d, '__manifest__.py')):
            modules.append(d)

untested = []
tested = []

for mod in modules:
    test_dir = os.path.join(mod, 'tests')
    has_tests = False
    if os.path.exists(test_dir):
        # Check if there are python files in tests/
        files = [f for f in os.listdir(test_dir) if f.endswith('.py') and f != '__init__.py']
        if files:
            has_tests = True
            
    if has_tests:
        tested.append(mod)
    else:
        untested.append(mod)

print(f"Total modules: {len(modules)}")
print(f"Tested modules: {len(tested)}")
print(f"Untested modules: {len(untested)}")
print("\nTop 20 Untested Modules:")
for mod in untested[:20]:
    print(f"- {mod}")
