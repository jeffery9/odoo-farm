import os

all_modules = set()
for d in os.listdir('.'):
    if os.path.isdir(d) and os.path.exists(os.path.join(d, '__manifest__.py')):
        all_modules.add(d)

print(f"Total modules: {len(all_modules)}")

# We can query docker-compose test_farm_full or just write a script to see what fails
