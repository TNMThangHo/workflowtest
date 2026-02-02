import subprocess
import sys
with open("val_out.txt", "w", encoding='utf-8') as f:
    subprocess.run([sys.executable, "test-gen/validate_testcases.py", "--prd", "input/signupPrd.md", "--testcases", "output/updated_testcases_20260202_151142.md"], stdout=f, stderr=f, text=True)
