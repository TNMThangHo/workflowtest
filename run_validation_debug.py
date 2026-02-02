import subprocess
import sys

result = subprocess.run(
    [sys.executable, "test-gen/validate_testcases.py", 
     "--prd", "input/signupPrd.md",
     "--testcases", "output/updated_testcases_20260202_145017.md"],
    capture_output=True,
    text=True,
    cwd=r"d:\workflowTesting"
)

print("=== STDOUT ===")
print(result.stdout)
print("\n=== STDERR ===")
print(result.stderr)
print(f"\n=== EXIT CODE: {result.returncode} ===")
