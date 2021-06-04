#!/usr/bin/perl -w

use warnings;
use Linux::usermod;
use CGI;
use CGI::Session;
use utf8;

$q = CGI->new;

my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;
my $username = $session->param("username");

if (@autenticar eq 0) {
    $session->delete();
    $session->flush();
    print $q->redirect("https://nonuser.onthewifi.com/");
} elsif ($session->is_expired) {
    $session->delete();
    $session->flush();
    print $q->redirect("https://nonuser.onthewifi.com/");
} else {
    $password = $q->param('password1');
    $user = Linux::usermod->new($username);
    $user->set(password => $password);
    print $q->redirect ("https://nonuser.onthewifi.com/cgi-bin/account.cgi");
}