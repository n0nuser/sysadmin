function f_noNet {
    # Change root password
    passwd

    # Add admin user
    adduser admin

    # Locales
    echo "export LANGUAGE=es_ES.UTF-8
    export LANG=es_ES.UTF-8
    export LC_ALL=es_ES.UTF-8" >> /root/.bashrc
    
    # Hostname
    echo "piratebay" > /etc/hostname
    
    # Replacement for SSH
    sed -i '/#Port 22/c\Port 2222' /etc/ssh/sshd_config
    sed -i '/#LoginGraceTime 2m/c\LoginGraceTime 1m' /etc/ssh/sshd_config
    sed -i '/#MaxAuthTries 6/c\MaxAuthTries 3' /etc/ssh/sshd_config
    sed -i '/#MaxSessions 10/c\MaxSessions 4' /etc/ssh/sshd_config
    echo "Match Group usuarios
    ChrootDirectory %h/public_html
    X11Forwarding no
    AllowTcpForwarding no
    ForceCommand internal-sftp" >> /etc/ssh/sshd_config

    # Configure Static IP
    echo "auto eth0
    iface eth0 inet static
        address 192.168.1.10
        netmask 255.255.255.0
        gateway 192.168.1.1" > /etc/network/interfaces.d/eth0
    
    # Cloudfare DNS
    echo "nameserver 1.1.1.1" > /etc/resolv.conf

    # Hosts
    echo "127.0.0.1       localhost piratebay
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters" > /etc/hosts
}

function f_net {
    apt update -y && apt upgrade -y
    apt install net-tools locales sudo build-essential cpanminus libpam0g libpam0g-dev -y
    sed -i '/es_ES.UTF-8/s/^#//g' /etc/locale.gen
    locale-gen es_ES.UTF-8
    usermod -aG sudo admin
}


function f_certbot {
    # Instalación SSL
    apt update && apt install certbot python-certbot-apache -y
    certbot  --apache --redirect -d nonuser.onthewifi.com -m admin@nonuser.onthewifi.com --agree-tos
}

function f_webfiles {
    # Portal Web
    cp -r html/* /var/www/html/
    
    # CGIs
    cp -r cgi-bin/* /lib/cgi-bin/
        
    # Servicio chown
    mkdir /var/www/names/
    chown www-data:www-data /var/www/names/
    cp servicios/dirlookup /usr/bin/dirlookup
    chmod +x /usr/bin/dirlookup
    cp servicios/servicio /lib/systemd/system/dirlookupd.service
    systemctl enable dirlookupd.service
}

function f_permissions {
    # PAM login
    chmod u+s /usr/sbin/unix_chkpwd
    
    # CGIs
    chown www-data:www-data /lib/cgi-bin/*
    chmod +x /lib/cgi-bin/*

    # Passwd
    chgrp www-data /etc/passwd
    chmod 664 /etc/passwd

    # Shadow
    usermod -aG shadow www-data
    chmod 660 /etc/shadow

    # User directories
    chgrp www-data /home
    chmod 775 /home
}

function f_apache2 {
    apt install apache2 -y
    groupadd usuarios

    # Apache modules
    a2enmod cgid
    a2enmod ssl

    # Perl modules
    cpanm CGI
    cpanm Authen::PAM
    cpanm Sys::Load
    cpanm utf8
    cpanm File::Copy::Recursive
    cpanm Linux::usermod
    cpanm IPC::System::Simple

    f_certbot
    f_webfiles
    f_permissions
}

function f_mariadb {
    apt install mariadb-server -y
}

function f_postfix {
    apt install postfix -y
    # Edit main.cf 
    cp ficheros/postfix/main.cf /etc/postfix/main.cf
    # Routing from domain to localhost
    echo "@nonuser.onthewifi.com @localhost" > /etc/postfix/vmailbox
    postmap /etc/postfix/vmailbox
    # Edit master.cf 
    cp ficheros/postfix/master.cf /etc/postfix/master.cf

    systemctl restart postfix
}

function f_dovecot {
    apt install dovecot-imapd -y
    
    # Replace Mailbox with Maildir
    cp ficheros/dovecot/10-mail.conf /etc/dovecot/conf.d/10-mail.conf
    # Edit 10-master.conf
    cp ficheros/dovecot/10-master.conf /etc/dovecot/conf.d/10-master.conf
    # Uncomment and change 10-auth.conf
    sed -i '/disable_plaintext_auth = yes/s/^#//g' /etc/dovecot/conf.d/10-auth.conf
    sed -i '/auth_mechanisms = plain/c\auth_mechanisms = plain login'  /etc/dovecot/conf.d/10-auth.conf
    # Change 10-ssl.conf
    cp ficheros/dovecot/10-ssl.conf /etc/dovecot/conf.d/10-ssl.conf
    # Change auth-system.conf.ext
    cp ficheros/dovecot/auth-system.conf.ext /etc/dovecot/conf.d/auth-system.conf.ext

    systemctl restart dovecot
}

function f_roundcube {
    apt install roundcube -y
    # Link webmail directory to Apache Server
    ln -s /usr/share/roundcube/ /var/www/html/webmail
    # Copy config
    cp ficheros/roundcube/config.conf /etc/roundcube/config.inc.php
}

function f_fail2ban {
    apt install fail2ban -y
    
    # Configure jail.local
    cp ficheros/fail2ban/jail.local /etc/fail2ban/jail.local

    # Enable jails in Debian
    echo "[sshd]
enabled = true

[apache-auth]
enabled = true

[apache-badbots]
enabled = true

[apache-noscript]
enabled = true

[apache-overflows]
enabled = true

[apache-nohome]
enabled = true

[apache-botsearch]
enabled = true

[apache-fakegooglebot]
enabled = true

[apache-modsecurity]
enabled = true

[apache-shellshock]
enabled = true

[dovecot]
enabled = true

[postfix]
enabled = true

[postfix-rbl]
enabled = true

[postfix-sasl]
enabled = true

[roundcube-auth]
enabled = true" > /etc/fail2ban/jail.d/defaults-debian.confç

    systemctl restart fail2ban
 }

 function quota {
    apt install quota
 }

function main {
    read -p "Do you have internet? (Y/N): " yesNo
    if [ $yesNo = "Y" ] || [ $yesNo = "y" ]; then
        f_net
        f_mariadb
        f_apache2
        f_postfix
        f_dovecot
        f_roundcube
        f_fail2ban
        f_quota
    else
        f_noNet
    fi
}

main