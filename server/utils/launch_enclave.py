import securexgboost as xgb
import _thread
import multiprocessing
import sys

def launch(clients):
    # Launch enclave
    # print("launched enclave")
    enclave_image = "enclave/xgboost_enclave.signed"
    xgb.init_server(enclave_image=enclave_image, client_list=clients)

    # Launch RPC server
    # print("started enclave rpc server")
    # print(clients)
    xgb.serve(all_users=clients, port=50051)

if __name__ == "__main__":
    num_clients = len(sys.argv[1])
    a = sys.argv[1][1:num_clients - 1]
    clients_with_quotes = a.split(', ')
    clients = [client[1:len(client) - 1] for client in clients_with_quotes]
    launch(clients)
