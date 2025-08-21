#
# qdportscan.py, by Seb
# A quick&dirty script to wait for the target to go up and enumerate a bunch of ports to see if any are open
#

import os
import sys
import time
import socket
import threading

PORTS = [False for _ in range(1000)]
# PRINT_LOCK = threading.Lock()

PING_INTERVAL = 10
PORT_RANGE = 1000
NUM_THREADS = 50

def check_port(ip: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    port_open = result == 0
    sock.close()
    return port_open

def scan_thread(t: int, ip: str, start_port: int, num_ports: int):
    global PORTS#, PRINT_LOCK
    for p in range(num_ports):
        port = start_port + p + 1
        port_open = check_port(ip, port)
        PORTS[port-1] = port_open
        # with PRINT_LOCK:
        #     print(f"Thread {t+1}) Port {port} is", "open" if port_open else "closed")

def is_target_up(ip: str) -> bool:
    return os.system(f"ping -n 1 {ip}") == 0 # Cheeky: A nonzero status code means the target wasn't up

def main() -> None:
    _, ip, outdir = sys.argv

    # Wait for target to go up
    print("Waiting for target to go up.", end="")
    while not is_target_up(ip):
        print(".", end="")
        time.sleep(PING_INTERVAL)
    print(" Target up!")

    print("Beginning portscan...")
    threads = []
    ports_per_thread = PORT_RANGE // NUM_THREADS
    for t in range(NUM_THREADS):
        print(f"Thread {t+1} is in charge of ports {t*ports_per_thread} to {t*ports_per_thread+ports_per_thread}")
        threads.append(threading.Thread(target=scan_thread, args=(t, ip, t*ports_per_thread, ports_per_thread)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Portscan done! Results below:")
    for i, p in enumerate(PORTS):
        if p:
            print(f"Port {i+1} is up!")

if __name__ == "__main__":
    main()
