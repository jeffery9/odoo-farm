# -*- coding: utf-8 -*-
import os
import py_compile

def check_workspace_syntax():
    print("🔍 Checking Python syntax for all files in the workspace...")
    errors_found = 0
    base_dir = "/Users/jeffery/odoo-farm-workspace/odoo-farm-dev"
    
    for root, dirs, files in os.walk(base_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.py'):
                fpath = os.path.join(root, file)
                try:
                    py_compile.compile(fpath, doraise=True)
                except py_compile.PyCompileError as e:
                    print(f"❌ Syntax Error found in: {fpath}")
                    print(e)
                    errors_found += 1
                except Exception as e:
                    print(f"⚠️ Error compiling {fpath}: {e}")
                    errors_found += 1
                    
    if errors_found == 0:
        print("🎉 Perfect! Every single Python file in the workspace is syntactically correct!")
    else:
        print(f"🚨 Found {errors_found} syntax errors in the workspace!")

if __name__ == "__main__":
    check_workspace_syntax()
