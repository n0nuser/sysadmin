#!/usr/bin/perl -w

use warnings;
use Linux::usermod;
use CGI;
use CGI::Cookie;
use utf8;
use File::Copy::Recursive;

$q = CGI->new;

%cookies = CGI::Cookie->fetch;
$username = $cookies{'campurriana'}->value;
$password = $q->param('password1');
$user = Linux::usermod->new($username);
$user->set(password => $password);

print $q->redirect ( -url => "https://nonuser.onthewifi.com/cgi-bin/account.cgi", -cookie => $cookie );
