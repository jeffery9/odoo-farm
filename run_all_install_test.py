import os
import subprocess
import sys

# Check for CI mode
is_ci = '--ci' in sys.argv

# Gather all module names
modules = [d for d in os.listdir('.') if os.path.isdir(d) and (d.startswith('farm_') or d.startswith('agri_') or d.startswith('precision_'))]
modules.sort()
modules_str = ','.join(modules)

print(f"Installing and testing {len(modules)} modules...")

# Construct the docker compose command
# We use --log-level=test to ensure test logs are fully captured.
cmd = [
    "docker", "compose", "run", "--rm", "web", "odoo", 
    "-d", "test_stdd_db_final", 
    "-i", modules_str, 
    "--test-enable", 
    "--stop-after-init", 
    "--log-level=test"
]

has_error = False
log_lines = []

try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    for line in iter(process.stdout.readline, ''):
        stripped_line = line.strip()
        log_lines.append(stripped_line)
        
        # In CI mode, print everything so we have a full artifact log
        if is_ci:
            print(stripped_line)
        else:
            # In local mode, only keep the last 50 lines to avoid flooding the terminal
            if len(log_lines) > 50:
                log_lines.pop(0)

        # STRICT HARDENING: Odoo sometimes exits with 0 even if an ERROR occurred in a sub-thread or test.
        # We manually scan the logs for critical failure signatures.
        if " ERROR " in stripped_line or " CRITICAL " in stripped_line or "Traceback (most recent call last):" in stripped_line:
            # Ignore some known non-fatal Odoo base errors if necessary, but generally ERROR means failure
            has_error = True

    process.stdout.close()
    return_code = process.wait()
    
    if return_code == 0 and not has_error:
        print("\n\n✅ SUCCESS! All modules installed and tested without errors.")
        sys.exit(0)
    else:
        print(f"\n\n❌ FAILED! Exit code: {return_code}. Log scanned errors: {has_error}")
        if not is_ci:
            print("Last 50 lines of log:")
            for line in log_lines:
                print(line)
        sys.exit(1)
            
except Exception as e:
    print(f"Execution failed: {e}")
    sys.exit(1)
