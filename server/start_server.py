import subprocess
import argparse
import time
import sys
import os
import securexgboost as xgb

# Function to start the server enclave and orchestrator
running_processes = []
def start_server(clients):
    global running_processes

    if running_processes:
        for ps in running_processes:
            ps.kill()
        running_processes = []

    enclave = ["python3", "utils/launch_enclave.py", str(clients)]
    orchestrator = ["python3", "utils/start_orchestrator.py", str(clients)]

    process = subprocess.Popen(enclave, preexec_fn=os.setsid)
    running_processes.append(process)

    process2 = subprocess.Popen(orchestrator, preexec_fn=os.setsid)
    running_processes.append(process2)
    print("Started server for " + str(clients))

# Function to stop the server
def stop_server():
    global running_processes

    if running_processes:
        for ps in running_processes:
            ps.kill()
        running_processes = []

# Call the functions
prev_clients = ["user1", "user2"]
while True:
    clients = input(f"\nEnter client names, separted by space. Just press enter to repeat previous clients {prev_clients}: ")
    if clients:
        clients = clients.strip().split()
        prev_clients = clients
    else:
        clients = prev_clients
    start_server(clients)
    time.sleep(2)
    cont = input("\nEnter Y/y if you want to stop the server: ")
    if cont == 'Y' or cont == 'y':
        stop_server()
        break
