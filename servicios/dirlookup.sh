#!/bin/sh

while true; do
    dirNew="/var/www/nameNew/"
    dirDel="/var/www/nameDel/"

    soft="50M"
    hard="80M"
    
    sleep 1
    # New Users
    for file in $(ls $dirNew); do
        mkdir /home/$file
        chmod 755 /home/$file
        cp -r /etc/skel/* /home/$file/
        chown -R $file:usuarios /home/$file
        echo "[NEW][$(date "+%H:%M:%S %d-%m-%Y")] $file" >> /home/admin/usuarios.log
        rm "$dirNew$file"
        setquota -u $file $soft $hard 0 0 /
    done
    # Deleted Users
    for file in $(ls $dirDel); do
        echo "[DEL][$(date "+%H:%M:%S %d-%m-%Y")] $file" >> /home/admin/usuarios.log
        rm "$dirDel$file"
        rm -r /home/$file
    done
done