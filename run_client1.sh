#!/bin/sh

docker start user1 2>/dev/null || docker run --rm --name user1 -itdv $PWD/client1:/home/secure-xgboost -p 8081:80 -w /home/secure-xgboost/ sec-xgb:client
docker exec -it user1 bash -c "export LANG=C.UTF-8 && streamlit run Home.py"
docker stop user1
# docker attach user1

# read -rep $'\nGenerate certificates, encrypt data and transfer it? (y/[n]) ' response
# if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
# then
#     docker exec -it user1 python3 encrypt.py
#     read -rep $'\nPress enter to transfer encrypted data '
#     docker exec -it user1 python3 transfer_data.py
#     read -rep $'\nStart client collaboration? (y/[n]) ' response
#     if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
#     then
#       docker exec -it user1 python3 client_collaboration.py --config config/config.ini
#     else
#       echo -e "\nExiting..."
#       # docker stop user1
#     fi
# else
#   read -rep $'\nStart client collaboration? (y/[n]) ' response
#   if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
#   then
#     docker exec -it user1 python3 client_collaboration.py --config config/config.ini
#   else
#     echo -e "\nExiting..."
#     # docker stop user1
#   fi
# fi
