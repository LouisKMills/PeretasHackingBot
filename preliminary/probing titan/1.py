import sys
import os

data = sys.stdin.readline().strip()
print("Input:", data)

os.system("whoami")
os.system("ifconfig")

os.system("pwd")
os.system("ls")