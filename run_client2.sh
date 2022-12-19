#!/bin/sh

docker start user2 2>/dev/null || docker run --rm --name user2 -itdv $PWD/client2:/home/secure-xgboost -p 8082:80 -w /home/secure-xgboost/ sec-xgb:client
docker exec -it user2 bash -c "export LANG=C.UTF-8 && streamlit run Home.py"
docker stop user2

# read -rep $'\nGenerate certificates, encrypt data and transfer it? (y/[n]) ' response
# if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
# then
#     docker exec -it user2 python3 encrypt.py
#     read -rep $'\nPress enter to transfer encrypted data '
#     docker exec -it user2 python3 transfer_data.py
#     read -rep $'\nStart client collaboration? (y/[n]) ' response
#     if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
#     then
#       docker exec -it user2 python3 client_collaboration.py --config config/config.ini
#     else
#       echo -e "\nExiting..."
#       # docker stop user2
#     fi
# else
#   read -rep $'\nStart client collaboration? (y/[n]) ' response
#   if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
#   then
#     docker exec -it user2 python3 client_collaboration.py --config config/config.ini
#   else
#     echo -e "\nExiting..."
#     # docker stop user2
#   fi
# fi
