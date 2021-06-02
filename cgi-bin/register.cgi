#!/usr/bin/perl -w

use warnings;
use Linux::usermod;
use CGI;
use CGI::Cookie;
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

if($username eq "root"){
   print("That user is already taken<br>");
   exit(1);
}

Linux::usermod->add($username, $password, '', $group, '', $directory, $shell);
($name, $pass, $uid, $gid, $quota, $comment, $gcos, $dir, $shell, $expire) = getpwnam($username);

mkdir "$directory",0755 or print "Directory cannot be created: $!<br>";
File::Copy::Recursive::dircopy("/etc/skel",$directory) or print "Cannot copy Skel files to $name\'s home: $!<br>";

$chownFile="/var/www/nameNew/$username";
open(FH, '>', $chownFile) or print "Failed to create empty: $!\n";
close(FH);

my $cookie = $q->cookie( -name => "campurriana", -value => $username, -path => "/" );
print $q->redirect ( -url => "https://nonuser.onthewifi.com/cgi-bin/dashboard.cgi", -cookie => $cookie );