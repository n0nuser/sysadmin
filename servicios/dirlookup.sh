#!/bin/sh

dirNew="/var/www/nameNew/"
dirDel="/var/www/nameDel/"

soft_limit = "50M"
hard_limit = "80M"

while true; do
    sleep 1
    # New Users
    for file in $(ls $dirNew); do
        chown -R $file:usuarios /home/$file
        echo "[NEW][$(date "+%H:%M:%S %d-%m-%Y")] $dirNew$file" >> /home/admin/usuarios.log
        rm "$dirNew$file"
        setquota -u $file $soft_limit $hard_limit 0 0 /
    done
    # Deleted Users
    for file in $(ls $dirDel); do
        echo "[DEL][$(date "+%H:%M:%S %d-%m-%Y")] $dirDel$file" >> /home/admin/usuarios.log
        rm "$dirDel$file"
        deluser $file
        rm -r /home/$file
    done
done