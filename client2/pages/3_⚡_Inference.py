import os
import sys
import time
import subprocess
import pandas as pd
import streamlit as st
import securexgboost as xgb
from Utils import *
from sklearn.metrics import classification_report, confusion_matrix

# Sidebar
st.sidebar.title('CLIENT APP')
st.sidebar.markdown('#####') # Just for adding whitespace

if 'client_name' not in st.session_state or not st.session_state.client_name or not st.session_state.other_clients:
    st.error("Please enter client names first")
elif 'train' not in st.session_state or not st.session_state.train:
    st.error("Please train the model first")
else:
    st.sidebar.code("Server IP: " + st.session_state.server_ip)
    st.sidebar.code("Client: " + st.session_state.client_name)
    st.sidebar.code("Other client(s): " + st.session_state.other_clients)
    st.subheader("Inference")
    st.markdown('#####') # Just for adding whitespace
    if 'option' not in st.session_state:
        st.session_state.option = None
    if 'test_transfer' not in st.session_state:
        st.session_state.test_transfer = False
    if 'infer' not in st.session_state:
        st.session_state.infer = False

    # Create config file
    client = st.session_state.client_name
    other_clients = st.session_state.other_clients
    OUTPUT_DIR = "config/"
    config_file = OUTPUT_DIR+"config.ini"
    DATA_DIR = "data/"
    KEY_FILE = OUTPUT_DIR+f"{client}.txt"
    SERVER_DIR = "/home/secure-xgboost/central/"
    other_clients = other_clients.strip().split()
    users = [client] + other_clients
    users = sorted(users)

    # Selecting data
    st.markdown("#### Selecting data")
    st.info('Please note that the labels will not be shared with the server.')
    option = st.radio("Do you want to just predict or generate classification report?",
             ('Only Predict', 'Generate Classification Report'))
    if option == 'Only Predict':
        st.session_state.option = 'Only Predict'
        st.warning("Upload only .csv files with rows of '[features]', and without header/column names.")
    else:
        st.session_state.option = 'Generate Classification Report'
        st.warning("Upload only .csv files with rows of 'label + [features]', and without header/column names.")

    test_file = st.file_uploader("Testing data", type='csv')

    if test_file:
        if st.button('Encrypt and Transfer'):
            # Save data
            test_path = DATA_DIR + client + "-test"
            if st.session_state.option == 'Only Predict':
                with open(test_path + '.csv', 'wb') as f:
                    f.write(test_file.getbuffer())
            if st.session_state.option == 'Generate Classification Report':
                df_test = pd.read_csv(test_file, header=None)
                st.session_state.y_test = df_test[0].to_numpy()
                df_test = df_test.iloc[:, 1:]
                df_test.to_csv(test_path + ".csv", header=False, index=False)
            # Encrypt
            with st.spinner("Encrypting data..."):
                time.sleep(1)
                xgb.encrypt_file(test_path + '.csv', test_path + '.enc', KEY_FILE)
                st.success("Encryption complete")
            # Transfer
            with st.spinner("Transferring data to server..."):
                time.sleep(2)
                if isinstance(st.session_state.server_ip, str):
                    nodes = [st.session_state.server_ip]
                else:
                    nodes = st.session_state.server_ip
                for n in nodes:
                    transfer_data(test_path + ".enc", n)
                st.session_state.test_transfer = True
                st.success("Data shared successfully")

    elif st.session_state.test_transfer:
        st.success("Data already shared")

    # Predicting
    if st.session_state.test_transfer:
        st.markdown("#### Getting Inference")

        booster = st.session_state.model
        dtests = []
        if st.button('Predict'):
            with st.spinner("Loading testing matrices, waiting for other clients to reach the same step"):
                time.sleep(1)
                for user in users:
                    dtests.append(xgb.DMatrix({user: SERVER_DIR + f"{user}-test.enc?format=csv"}))
                st.success("Loaded testing data successfully")
            st.info("Inferencing will only start once all clients reach to this step")
            with st.spinner("Predicting..."):
                for i, dtest in enumerate(dtests):
                    predictions, num_preds = booster.predict(dtest, decrypt=False)
                    if i == users.index(client):
                        client_pred = predictions
                        client_num_preds = num_preds
                # Decrypt predictions
                pred_prob = booster.decrypt_predictions(client_pred, client_num_preds)

                # For binary classification
                threshold = 0.5
                st.session_state.y_pred = [0 if prob<=threshold else 1 for prob in pred_prob]
                if st.session_state.option == 'Only Predict':
                    y_pred = st.session_state.y_pred
                    st.markdown("##### Predictions: ")
                    st.download_button('Download Predictions', str(y_pred), file_name="predictions.txt")
                else:
                    st.markdown("##### Predictions: ")
                    y_pred = st.session_state.y_pred
                    y_test = st.session_state.y_test
                    st.download_button('Download Predictions', str(y_pred), file_name="predictions.txt")
                    cr_dict = classification_report(y_test, y_pred, output_dict=True)
                    st.session_state.acc = cr_dict.pop('accuracy')
                    st.markdown("##### Accuracy: ")
                    st.write(f"{st.session_state.acc*100:.2f}%")
                    st.markdown("##### Classification Report:")
                    st.session_state.cr = pd.DataFrame(cr_dict).T
                    st.table(st.session_state.cr)
                    st.session_state.cm = pd.DataFrame(confusion_matrix(y_test, y_pred),\
                                        index = [i for i in "01"], columns = [i for i in "01"])
                    st.markdown("##### Confusion Matrix:")
                    st.dataframe(st.session_state.cm)
                st.success("Prediction completed")
            st.session_state.infer = True
        elif st.session_state.infer:
            if st.session_state.option == 'Only Predict':
                st.success("Predicted already")
                st.markdown("##### Predictions: ")
                st.download_button('Download Predictions', str(st.session_state.y_pred), file_name="predictions.txt")
            else:
                st.success("Classification report already generated")
                st.markdown("##### Predictions: ")
                st.download_button('Download Predictions', str(st.session_state.y_pred), file_name="predictions.txt")
                st.markdown("##### Accuracy:")
                st.write(f"{st.session_state.acc*100:.2f}%")
                st.markdown("##### Classification Report:")
                st.table(st.session_state.cr)
                st.markdown("##### Confusion Matrix:")
                st.dataframe(st.session_state.cm)
