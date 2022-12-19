import os
import sys
import time
import subprocess
import streamlit as st
import securexgboost as xgb

# Running processes saved in the session state
if 'running_processes' not in st.session_state:
    st.session_state.running_processes = []

running_processes = st.session_state.running_processes

# Starts the server for the required clients
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

# Streamlit app
st.sidebar.title('SERVER APP')
st.sidebar.markdown('#####') # Just for adding whitespace

# Server IP address
with open("hosts.config") as f:
    ip = f.read()
    ip = ip[:ip.rfind(':')]
st.sidebar.caption("Server IP address")
st.sidebar.code(ip)

# Select the mode
mode = st.sidebar.selectbox("Select the server mode", ("Training", "Inference"))

# Configuring the clients participating
st.subheader("Server Configuration")
if mode == "Training":
    clients = st.text_input("Enter the client name(s) [separated by a space]")
    clients = clients.strip().split()
elif mode == "Inference":
    clients = st.text_input("Enter the client name")
    if len(clients.strip().split()) > 1:
        st.error("You can only add one client when inferencing! Please remove extra users.")
        st.stop()

# After client names added
if clients:
    st.markdown('#####') # Just for adding whitespace
    if st.button('Start server'):
        with st.spinner('Waiting...'):
            start_server(clients)
            st.session_state.running_processes = running_processes
            time.sleep(2)
        st.success("Server started successfully!")
