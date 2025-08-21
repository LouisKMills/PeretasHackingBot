#!/usr/bin/python3
import sys
import time
import subprocess

def main() -> None:
    # Boy I hope we get exactly 2 args lol
    print("argv:", sys.argv)
    ip = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."

    start_time = time.time()
    nmap_run = subprocess.run(["nmap", ip], shell=True, capture_output=True)
    end_time = time.time()
    print("Nmap ran with time", end_time-start_time, "seconds")
    
    try: print("## stdout:", nmap_run.stdout.decode())
    except Exception as e: print("## stdout: Couldn't decode :(", e)

    try: print("## stderr:", nmap_run.stderr.decode())
    except Exception as e: print("## stderr: Couldn't decode :(", e)
    
    print(nmap_run)

if __name__ == "__main__":
    main()