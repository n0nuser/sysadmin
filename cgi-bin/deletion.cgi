#!/usr/bin/perl -w

use warnings;
use Linux::usermod;
use CGI;
use utf8;
use File::Copy::Recursive;

$q = CGI->new;
$username = lc($q->param('username'));
$password = $q->param('password');
$email = $q->param('email');
$name = $q->param('name');
$surname = $q->param('surname');

$directory = "/home/$username";
$group = "1001";
$shell = "/usr/sbin/nologin";

print $q->header;

if($username eq "root"){
   print("That user is already taken<br>");
   exit(1);
}

Linux::usermod->del($username);

$delUser="/var/www/nameDel/$username";
open(FH, '>', $delUser) or print "Failed to create empty: $!\n";
close(FH);

print('Usuario borrado satisfactoriamente.<br>Vuelva a la <a href="">pantalla de inicio</a>');