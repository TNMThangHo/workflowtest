import subprocess
import sys

result = subprocess.run(
    [sys.executable, "test-gen/validate_testcases.py", 
     "--prd", "input/signupPrd.md",
     "--testcases", "output/updated_testcases_20260202_151142.md"],
    capture_output=True,
    text=True,
    cwd=r"d:\workflowTesting"
)

print(f"EXIT CODE: {result.returncode}")
print("=== STDOUT ===")
print(result.stdout)
print("=== STDERR ===")
print(result.stderr)
