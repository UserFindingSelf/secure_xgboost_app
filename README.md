# Secure XGBoost Colloboration App
A Secure XGBoost application, created using Streamlit. Using this, you can securely train models and get inference.
*This app simulates HW Enclaves to demonstrate how secure collaboration works.*

## Pre requisites
1. Linux (at least 18.04 version)
2. Docker images for server and client

## Guide
1. Load docker images using `docker load image.tar`
2. Start server from terminal using `bash run_server.sh`
3. Add user names you want to run the server for (default: user1 & user2)
4. Start the client containers using `bash run_client1.sh` and `bash run_client2.sh` in two different terminal windows
5. Run the app by clicking on link present on terminal
6. Generate keys, train collaboratively, and get predictions with classification metrics through the app
