import os
import subprocess
import sys

# Gather all module names
modules = [d for d in os.listdir('.') if os.path.isdir(d) and (d.startswith('farm_') or d.startswith('agri_'))]
modules.sort()
modules_str = ','.join(modules)

print(f"Installing and testing {len(modules)} modules...")

# Construct the docker compose command
cmd = [
    "docker", "compose", "run", "--rm", "web", "odoo", 
    "-d", "test_stdd_db_final_v48", 
    "-i", modules_str, 
    "--test-enable", 
    "--stop-after-init", 
    "--log-level=info"
]

# Run the command with an extended timeout mechanism
# We pipe the output so we can see it progressing but also catch errors
try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    # We will print the last 1000 lines if it fails to ensure we capture the complete Odoo trace
    log_lines = []
    for line in iter(process.stdout.readline, ''):
        log_lines.append(line.strip())
        if len(log_lines) > 1000:
            log_lines.pop(0)
            
    process.stdout.close()
    return_code = process.wait()
    
    if return_code == 0:
        print("\n\nSUCCESS! All modules installed and tested without errors.")
    else:
        print(f"\n\nFAILED with exit code {return_code}.")
        print("Last 1000 lines of log:")
        for line in log_lines:
            print(line)
            
except Exception as e:
    print(f"Execution failed: {e}")

