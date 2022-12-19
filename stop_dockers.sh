#!/bin/sh

docker stop user1 user2 server
echo -e "\nContainers running:"
docker ps
