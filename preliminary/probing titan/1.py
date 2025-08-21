import sys
import subprocess

data = sys.stdin.readline().strip()
print("Input:", data)


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    print(result.stdout.strip())

run("whoami")
run("ifconfig")
run("pwd")
run("ls")