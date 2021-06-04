#!/bin/bash

while true; do
    # Variables
    sleepTime=1800 # Half an hour
    dir="/var/www/status/"
    declare -a services=("apache2" "sshd" "postfix" "dovecot" "mariadb" "quotaon" "dirlookupd" "statusd")

    for service in "${services[@]}"
    do
        (systemctl -q is-active $service && echo 1 || echo 0) > $dir$service
    done
    sleep $sleepTime
done