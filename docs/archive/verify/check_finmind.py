import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-c", "from FinMind.data import DataLoader; print('FinMind OK')"],
    capture_output=True, text=True, timeout=10
)
print(f"stdout: {result.stdout}")
print(f"stderr: {result.stderr}")
print(f"rc: {result.returncode}")
