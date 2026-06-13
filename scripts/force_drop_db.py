import subprocess
import time
import sys

def run_psql(cmd):
    full_cmd = ["docker", "compose", "exec", "-T", "db", "psql", "-U", "odoo", "-d", "postgres", "-c", cmd]
    return subprocess.run(full_cmd, capture_output=True, text=True)

print("Terminating all connections to test_stdd_db_final...")
run_psql("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'test_stdd_db_final' AND pid <> pg_backend_pid();")

print("Dropping database test_stdd_db_final...")
for i in range(5):
    res = run_psql("DROP DATABASE IF EXISTS test_stdd_db_final;")
    if res.returncode == 0:
        print("Database dropped successfully.")
        break
    else:
        print(f"Attempt {i+1} failed: {res.stderr.strip()}")
        run_psql("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'test_stdd_db_final' AND pid <> pg_backend_pid();")
        time.sleep(1)
else:
    print("Failed to drop database after 5 attempts.")
    sys.exit(1)
