#!/bin/sh

docker start server 2>/dev/null || docker run -u 0 --rm --name server -itdv $PWD/server:/home/secure-xgboost -p 5000:5000 -w /home/secure-xgboost/ sec-xgb:server

# Starts the ssh for data transfer through scp
docker exec -itd server service ssh restart

# Saving server IP address
docker inspect server | grep '"IPAddress"' | awk 'NR==1{print(substr($2, 2, length($2)-3)":22")}' > server/hosts.config

# Sharing IP address with clients
cp server/hosts.config client1/config/hosts.config
cp server/hosts.config client2/config/hosts.config

# Running the start_server.py script in docker
docker exec -it server bash -c "python3 start_server.py"
docker stop server
