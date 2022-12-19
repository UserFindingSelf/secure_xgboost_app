import os
import sys
import time
import subprocess
import streamlit as st
import securexgboost as xgb
from Utils import *

# Sidebar
st.sidebar.title('CLIENT APP')
st.sidebar.markdown('#####') # Just for adding whitespace

if 'client_name' not in st.session_state or not st.session_state.client_name or not st.session_state.other_clients:
    st.error("Please enter client names first")
else:
    client = st.session_state.client_name
    if 'option' not in st.session_state:
        st.session_state.option = ''
    if 'key' not in st.session_state:
        st.session_state.key = False

    st.sidebar.code("Server IP: " + st.session_state.server_ip)
    st.sidebar.code("Client: " + st.session_state.client_name)
    st.sidebar.code("Other client(s): " + st.session_state.other_clients)
    st.subheader("Keys and Certificate")
    st.markdown('#####') # Just for adding whitespace

    option = st.radio(
         "Do you want to generate new keys and certificate or use saved ones?",
         ('Generate New', 'Use Saved'))

    if st.button(option):
        st.session_state.option = option
        st.session_state.key = False

    if not st.session_state.key:
        st.info("If you don't select any of the two options, then default keys and certificate will be used.")
        if st.session_state.option == 'Generate New':
            # Generating certificates and keys in config/
            generate_certificate(client)
            KEY_FILE = f"config/{client}.txt"
            xgb.generate_client_key(KEY_FILE)
            st.success("Keys generated successfully")
            st.session_state.key = True

        elif st.session_state.option == 'Use Saved':
            st.info('All files should have the right extensions!')
            st.markdown("\
            - **.pem** -> Private Client Key \n\
            - **.crt** -> Public Client Signing Certificate \n\
            - **.txt** -> Symmetric Client Key")
            # Use saved keys
            DIR = "config/"
            extensions = ['pem', 'crt', 'txt']
            files = st.file_uploader("Add all files below", accept_multiple_files=True)
            up_ext = []
            for file in files:
                ext = file.name.split('.')[1]
                if ext not in extensions:
                    st.error(f"File with wrong extension chosen! Please check.")
                    st.stop()
                if ext in up_ext:
                    st.error(f"File with same extension chosen! Please check.")
                    st.stop()
                up_ext.append(ext)

            if len(files) != 3:
                st.warning("Please upload exactly 3 files")
            else:
                # Saving selected keys to config/
                if st.button('Select'):
                    for file in files:
                        ext = file.name.split('.')[1]
                        with open(DIR + client + '.' + ext, 'wb') as f:
                            f.write(file.getbuffer())
                    st.success("Keys and certificate selected successfully")
                    st.session_state.key = True
    else:
        st.success(f"Keys and certificate already selected using '{st.session_state.option}' option")
