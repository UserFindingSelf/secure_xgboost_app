import os
import sys
import time
import subprocess
import streamlit as st
import securexgboost as xgb

# Streamlit app
st.set_page_config(
    page_title="Homepage",
)

if 'server' not in st.session_state:
    st.session_state.server = True
if 'client_name' not in st.session_state:
    st.session_state.client_name = ''
if 'other_clients' not in st.session_state:
    st.session_state.other_clients = ''

# Sidebar
CLIENT = "user2"
OTHER_CLIENT = "user1"
HOSTS_FILE = "config/hosts.config"
with open(HOSTS_FILE) as f:
    nodes = f.readlines()
if not nodes:
    st.error("Can't connect to server. Try again.")
    st.stop()
elif len(nodes) == 1:
    st.session_state.server_ip = nodes[0].strip().split(":")[0]
else:
    st.session_state.server_ip = str([x.strip().split(":")[0] for x in nodes])

# Main page
st.sidebar.title('CLIENT APP')
st.sidebar.markdown('#####') # Just for adding whitespace
if st.session_state.server:
    st.session_state.server = False
    with st.spinner('Connecting to server...'):
        time.sleep(1)
st.sidebar.code("Server IP: " + st.session_state.server_ip)
st.subheader("Client Configuration")

client = st.text_input("Your client name", value=CLIENT)
# Client name added
if client:
    st.session_state.client_name = client
    st.success("Name saved as '" + st.session_state.client_name + "'")
elif st.session_state.client_name:
    st.success("Name saved as '" + st.session_state.client_name + "'")
st.sidebar.code("Client: " + st.session_state.client_name)

other_clients = st.text_input("Other client's name(s) [separated by space] or same client's name [if training alone]", value=OTHER_CLIENT)
# Other client name added
if other_clients:
    st.session_state.other_clients = other_clients
    st.success("Other client(s): '" + st.session_state.other_clients + "'")
elif st.session_state.other_clients:
    st.success("Other client(s): '" + st.session_state.other_clients + "'")
st.sidebar.code("Other client(s): " + st.session_state.other_clients)
