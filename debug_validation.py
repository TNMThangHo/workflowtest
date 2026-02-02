import subprocess
import sys

result = subprocess.run(
    [sys.executable, "test-gen/validate_testcases.py", 
     "--prd", "input/signupPrd.md",
     "--testcases", "output/test_cases.md"],
    capture_output=True,
    text=True,
    cwd=r"d:\workflowTesting"
)

with open("d:/workflowTesting/validation_full_output.txt", "w", encoding="utf-8") as f:
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n\n=== STDERR ===\n")
    f.write(result.stderr)
    f.write(f"\n\n=== EXIT CODE: {result.returncode} ===\n")

print("Output saved to validation_full_output.txt")
print(f"Exit code: {result.returncode}")
print("\n=== STDOUT (first 1000 chars) ===")
print(result.stdout[:1000] if result.stdout else "(empty)")
print("\n=== STDERR (first 500 chars) ===")
print(result.stderr[:500] if result.stderr else "(empty)")
