#!/usr/bin/perl -w

use warnings;
use CGI;
use CGI::Cookie;
use CGI::Session;
use utf8;

$q = CGI->new;

#Crear un objeto session
my $session = new CGI::Session;

#Cargamos datos de la session
$session->load();

$session->delete();
$session->flush();

print $q->redirect("https://nonuser.onthewifi.com/");
