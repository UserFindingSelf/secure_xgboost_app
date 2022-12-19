import securexgboost as xgb
import sys

def start_rpc_orchestrator(clients):
    # print("start rpc orchestrator")
    with open("hosts.config") as f:
    	nodes = f.readlines()
    nodes = [x.strip().split(":")[0] for x in nodes]
    # print(clients)
    xgb.serve(all_users=clients, nodes=nodes, port=50052)

if __name__ == "__main__":
    num_clients = len(sys.argv[1])
    a = sys.argv[1][1:num_clients - 1]
    clients_with_quotes = a.split(', ')
    clients = [client[1:len(client) - 1] for client in clients_with_quotes]
    start_rpc_orchestrator(clients)
