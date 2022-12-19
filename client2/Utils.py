import subprocess
import sys
import securexgboost as xgb

def run_subprocess(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, b''):
        line = line.decode("utf-8")
        sys.stdout.write(line)

def transfer_data(data, ip):
    print("Transferring {} to {}".format(data[data.rfind('/')+1:], ip))
    cmd = ["scp", "-o", "StrictHostKeyChecking=no",# "-o", "UserKnownHostsFile=/dev/null",
                    data, "root@{}:/home/secure-xgboost/central/".format(ip)]
    run_subprocess(cmd)

def generate_certificate(username):
    cmd = ["./config/gen-client.sh", username]
    run_subprocess(cmd)

def create_client_config(output_dir, user, other_clients, PRIV_KEY, CERT_FILE, KEY_FILE, PORT):
    HOSTS_FILE = "config/hosts.config"
    with open(HOSTS_FILE) as f:
        nodes = f.readlines()
    nodes = [x.strip().split(":")[0] for x in nodes]
    NODE_IP = nodes[0] # First IP address
    REMOTE_ADDR = NODE_IP+':'+PORT

    # Create config.ini file
    assert output_dir[-1] == '/', "Output directory address should end with /"
    with open(output_dir + "config.ini", 'w') as f:
        f.write("[default]\n\n")
        f.write("user_name = " + user + "\n")
        f.write("sym_key_file =  " + KEY_FILE + "\n")
        f.write("priv_key_file = " + PRIV_KEY + "\n")
        f.write("cert_file = " + CERT_FILE + "\n")
        f.write("remote_addr = " + REMOTE_ADDR + "\n")
        f.write("client_list = " + other_clients + "\n")
