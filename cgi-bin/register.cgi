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

Linux::usermod->add($username, $password, '', $group, '', $directory, $shell);
($name, $pass, $uid, $gid, $quota, $comment, $gcos, $dir, $shell, $expire) = getpwnam($username);

mkdir "$directory",0755 or print "Directory cannot be created: $!<br>";
File::Copy::Recursive::dircopy("/etc/skel",$directory) or print "Cannot copy Skel files to $name\'s home: $!<br>";

$chownFile="/var/www/names/$username";
open(FH, '>', $chownFile) or print "Failed to create empty: $!\n";
close(FH);

print "<h1>Datos:</h1><br>Name: $name<br>Password: $pass<br>UID: $uid<br>GID: $gid<br>Quota: $quota<br>Shell: $shell<br>Home: $dir<br>";