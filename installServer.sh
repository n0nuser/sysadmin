function f_noNet {
    # Change root password
    passwd

    # Skel
    mkdir /etc/skel/Maildir
    mkdir /etc/skel/public_html

    cp -r ficheros/public_html/* /etc/skel/public_html/

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

    # Configure Static IP
    echo "auto eth0
    iface eth0 inet static
        address 192.168.1.10
        netmask 255.255.255.0
        gateway 192.168.1.1" > /etc/network/interfaces.d/eth0
    
    # Cloudfare DNS
    echo "nameserver 1.1.1.1" > /etc/resolv.conf

    # Hosts
    echo "127.0.0.1       nonuser.onthewifi.com localhost piratebay
::1             nonuser.onthewifi.com localhost piratebay ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters" > /etc/hosts
}

function f_net {
    apt update -y && apt upgrade -y
    apt install net-tools locales jq sudo build-essential pkg-config libgd-dev git cmake cpanminus ufw libpam0g libpam0g-dev libmariadb-dev -y
    sed -i '/es_ES.UTF-8/s/^#//g' /etc/locale.gen
    locale-gen es_ES.UTF-8
    usermod -aG sudo admin
    timedatectl set-timezone "Europe/Madrid"
}


function f_ssh {
    cp ficheros/ssh/sshd_config /etc/ssh/sshd_config
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

    # Servicio chown
    mkdir /var/www/nameNew/
    mkdir /var/www/nameDel/
    mkdir /var/www/status
    chown www-data:www-data /var/www/nameNew/
    chown www-data:www-data /var/www/nameDel/
    chown www-data:www-data /var/www/status/
    
    cp servicios/dirlookup /usr/bin/dirlookup
    chmod +x /usr/bin/dirlookup
    cp servicios/dirlookupd.service /lib/systemd/system/dirlookupd.service
    systemctl enable dirlookupd.service

    cp servicios/status /usr/bin/status
    chmod +x /usr/bin/status
    (crontab -l 2>/dev/null; echo "*/15 * * * * /usr/bin/status") | crontab -
    systemctl enable statusd.service

    # Pagina Admin
    cpanm ExtUtils::PkgConfig
    cpanm GD::Graph
}

function f_apache2 {
    apt install apache2 -y
    groupadd usuarios

    cp ficheros/apache/apache2.conf /etc/apache2/apache2.conf

    # Apache modules
    a2enmod cgid
    a2enmod ssl
    a2enmod userdir

    # Perl modules
    cpanm CGI
    cpanm CGI::Session
    cpanm Filesys::DiskUsage
    cpanm Proc::ProcessTable
    cpanm Crypt::RandPasswd
    cpanm Authen::PAM
    cpanm Sys::Load
    cpanm utf8
    cpanm File::Copy::Recursive
    cpanm Linux::usermod
    cpanm IPC::System::Simple
    cpanm DBD::mysql
    cpanm DBD::MariaDB
    cpanm SQL::Abstract
    cpanm File::Slurp
    cpanm Data::Dumper::Simple
    cpanm Email::MIME
    cpanm Email::Sender::Simple
    cpanm MIME::Words

    f_certbot
    f_webfiles
    f_permissions
}

function f_mariadb {
    apt install mariadb-server -y

    # Cambiar contraseña para root
    systemctl stop mysql
    systemctl stop mariadb
    mysqld_safe --skip-grant-tables --skip-networking &
    mysql -u root < ficheros/mariadb/createDB.sql
   
    # Crear base de datos Usuarios y tabla Datos
    mysql --user=root --password=admin < ficheros/mariadb/createDB.sql
    mysql --user=root --password=admin usuarios < ficheros/mariadb/createTable.sql
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
    cp ficheros/fail2ban/defaults-debian.conf > /etc/fail2ban/jail.d/defaults-debian.conf

    systemctl restart fail2ban
}

function f_quota {
    apt install quota -y
    # Edit /etc/fstab
    mount -o remount /
    quotacheck -gum /
    quotaon /
}

function f_rsyslog {
    # Logs de Apache
    echo 'module(load="imfile" PollingInterval="10")
input(type="imfile"
      File="/var/log/apache2/access.log"
      Tag="[APACHE]"
      Severity="error"
      Facility="local6")
local6.error        /home/admin/access.log' > /etc/rsyslog.d/02-apache.conf
    # Logs de correos
    echo "mail.*    -/home/admin/access.log" >> /etc/rsyslog.conf
    # Logs de autenticación por PAM (SSH, SFTP y Apache)
    echo "auth,authpriv.*                 -/home/admin/access.log" >> /etc/rsyslog.conf
    systemctl restart rsyslog
}


function f_wordpress {
    wget https://wordpress.org/latest.tar.gz
    tar -xzvf latest.tar .gz
    mv wordpress/ /var/www/html
    chown www-data:www-data /var/www/html/wordpress/*

    cp ficheros/apache/.htaccessWordpress > /var/www/html/wordpress/.htaccess
}

function f_tripwire {
    apt install tripwire -y
    tripwire --init
}

function f_monitorizacion {
    cp servicios/monitor.pl /usr/bin/monitor
    chmod +x /usr/bin/monitor
    (crontab -l 2>/dev/null; echo "0 8 * * * /usr/bin/monitor") | crontab -
}

function f_backup {
    mkdir /backups
    cp servicios/backup /usr/bin/backup
    (crontab -l 2>/dev/null; echo "0 4 * * * /usr/bin/backup") | crontab -
}

function f_mumble {
    # Install Docker
    curl -sSL https://get.docker.com/ | sh
	apt-get install docker-ce docker-ce-cli containerd.io -y

    # Install Mumble (ISO)
	docker run -d --name mumble -p 64738:64738  -p 64738:64738/udp ugeek/mumble:arm

    #Install NANO
    docker exec -i -t --user root mumble sh
    apk add nano

	# Manage Mumble with console
    #docker exec -i -t --user root mumble sh
    # Copy config file to Mumble
    docker cp ficheros/mumble/mumble-server.ini mumble:/config/mumble-server.ini

    # Servicio para Mumble
    cp servicios/mumble.service /lib/systemd/system/mumble.service
}

function main {
    read -p "Do you have internet? (Y/N): " yesNo
    if [ $yesNo = "Y" ] || [ $yesNo = "y" ]; then
        f_net
        f_ssh
        f_apache2
        f_mariadb
        f_postfix
        f_dovecot
        f_roundcube
        f_fail2ban
        f_quota
        f_rsyslog
        f_wordpress
        f_tripwire
        f_monitorizacion
        f_backup
        f_mumble
    else
        f_noNet
    fi
}

main