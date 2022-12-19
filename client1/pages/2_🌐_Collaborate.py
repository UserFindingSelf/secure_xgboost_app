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
    st.sidebar.code("Server IP: " + st.session_state.server_ip)
    st.sidebar.code("Client: " + st.session_state.client_name)
    st.sidebar.code("Other client(s): " + st.session_state.other_clients)
    st.subheader("Collaboration")
    st.markdown('#####') # Just for adding whitespace
    if 'train_transfer' not in st.session_state:
        st.session_state.train_transfer = False
    if 'train' not in st.session_state:
        st.session_state.train = False
    if 'model' not in st.session_state:
        st.session_state.model = None

    # Create config file
    client = st.session_state.client_name
    other_clients = st.session_state.other_clients
    OUTPUT_DIR = "config/"
    config_file = OUTPUT_DIR+"config.ini"
    DATA_DIR = "data/"
    PRIV_KEY = OUTPUT_DIR+f"{client}.pem"
    CERT_FILE = OUTPUT_DIR+f"{client}.crt"
    KEY_FILE = OUTPUT_DIR+f"{client}.txt"
    PORT = "50052"
    SERVER_DIR = "/home/secure-xgboost/central/"
    create_client_config(OUTPUT_DIR, client, other_clients, PRIV_KEY, CERT_FILE, KEY_FILE, PORT)

    # Selecting data
    st.info("Upload only .csv files with rows of 'label + [features]', and without header/column names.")
    st.markdown("#### Selecting data")
    train_file = st.file_uploader("Training data", type='csv')

    other_clients = other_clients.strip().split()
    users = [client] + other_clients
    users = sorted(users)

    if train_file:
        if st.button('Encrypt and Transfer'):
            # Save data
            train_path = DATA_DIR + client + "-train"
            with open(train_path + '.csv', 'wb') as f:
                f.write(train_file.getbuffer())
            # Encrypt
            with st.spinner("Encrypting data..."):
                time.sleep(1)
                xgb.encrypt_file(train_path + '.csv', train_path + '.enc', KEY_FILE)
                st.success("Encryption complete")
            # Transfer
            with st.spinner("Transferring data to server..."):
                time.sleep(2)
                if isinstance(st.session_state.server_ip, str):
                    nodes = [st.session_state.server_ip]
                else:
                    nodes = st.session_state.server_ip
                for n in nodes:
                    transfer_data(train_path + ".enc", n)
                st.session_state.train_transfer = True
                st.success("Data shared successfully")
    elif st.session_state.train_transfer:
        st.success("Data already shared")

    # Training
    if st.session_state.train_transfer:
        st.markdown("#### Training Model")

        # Set training parameters (make customizable)
        params = {
            "objective": "binary:logistic",
            "gamma": "0.1",
            "nthread": "4",
            "max_depth": "50",
            "eval_metric": ["logloss"] # , "auc"
        }
        num_rounds = st.number_input("Enter number of rounds:", min_value=1, max_value=100, value=50)

        if st.button('Start Training'):
            xgb.init_client(config=config_file)
            # Remote attestation
            with st.spinner("Remote attestation..."):
                time.sleep(1)
                # Note: Simulation mode does not support attestation pass in `verify=False` to attest()
                xgb.attest(verify=False)
                st.success("Report successfully verified")

            with st.spinner("Loading training matrices, waiting for other clients to reach the same step"):
                time.sleep(1)
                dtrain = xgb.DMatrix({user: SERVER_DIR + f"{user}-train.enc?format=csv&label_column=0" for user in users})
                st.session_state.train = dtrain
                st.success("Loaded training data successfully")

            st.info("Training will only start once all clients reach to this step")
            with st.spinner("Training..."):
                booster = xgb.train(params, dtrain, num_rounds, evals=[(dtrain, "train")])
                st.session_state.model = booster
                # model_file = f"{client}_model.txt"
                # with open(model_file, 'w') as f:
                #     f.writelines(booster.get_dump(decrypt=False))
                # st.write(booster.get_fscore())
                st.success("Model training complete")
            st.session_state.train = True

        elif st.session_state.train:
            st.success("Trained already")
            st.stop()
