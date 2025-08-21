#
# qdcommands.py, by Seb
# A basic script made just to test some of the capabilities of the machine our code will run on.
#

import sys
import time
import subprocess

def run_cmd(cmd_str, do_print=True) -> tuple:
    if type(cmd_str) == str:
        cmd = cmd_str.split()
    else:
        cmd = cmd_str

    start_time = time.time()
    nmap_run = subprocess.run(cmd, shell=True, capture_output=True)
    run_time = time.time() - start_time
    
    try: stdout = nmap_run.stdout.decode()
    except: stdout = None

    try: stderr = nmap_run.stderr.decode()
    except: stderr = None

    if do_print:
        print(f"=== `{cmd_str}` output:\n## stdout:\n{stdout}\n## stderr:\n{stderr}\n## runtime:\n{run_time} s\n")

    return stdout, stderr, run_time

def main() -> None:
    # Boy I hope we get exactly 2 args lol
    print("argv:", sys.argv)
    ip = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."

    run_cmd("ver") # Gets windows version
    run_cmd("whoami")
    run_cmd("echo %cd%") # pwd equivalent
    run_cmd("dir")
    run_cmd("ipconfig")
    run_cmd("echo %path%")
    run_cmd(["dir", "C:\\Users\\"])
    run_cmd(["dir", "C:\\Program Files\\"])
    run_cmd(["dir", "C:\\Program Files (x86)\\"])
    run_cmd("wsl -v")

if __name__ == "__main__":
    main()