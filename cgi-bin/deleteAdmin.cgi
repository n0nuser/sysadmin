#!/usr/bin/perl -w

use warnings;
use Linux::usermod;
use CGI;
use CGI::Session;
use utf8;
use SQL::Abstract;
use DBI;

# Base datos
$usuarioDB = "root";
$claveDB = "admin";
$DB = "usuarios";
$tabla = "datos";

$q = CGI->new;

# Gestión sesión
my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;
my $username = $session->param("username");

if (@autenticar eq 0)
{
    $session->delete();
    $session->flush();
    print $q->redirect("https://nonuser.onthewifi.com/");
}
elsif ($session->is_expired)
{
    $session->delete();
    $session->flush();
    print $q->redirect("https://nonuser.onthewifi.com/");
}
else
{
    if ($username eq "admin")
    {
        $user = $q->param("user");

        # No se permite borrar a Admin
        if($user ne "admin")
        {
            # Se borra al usuario
            Linux::usermod->del($user);

            # Se añade fichero para que servicio lo borre
            $delUser="/var/www/nameDel/$user";
            open(FH, '>', $delUser) or print "Failed to create empty: $!\n";
            close(FH);

            # Gestión Base Datos
            my $sql = SQL::Abstract->new;
            $dbh = DBI->connect("DBI:MariaDB:$DB:localhost", $usuarioDB, $claveDB) or die "\nError al abrir la base de datos.\n";
            my %where = (
                usuario => $user
            );
            my($stmt, @bind) = $sql->delete($tabla, \%where);
            my $sth = $dbh->prepare($stmt);
            $sth->execute(@bind);
            $dbh->disconnect or warn "\nFallo al desconectar.\n";
        }
        print $q->redirect("https://nonuser.onthewifi.com/cgi-bin/admin.cgi");
    }
    else
    {
        print $q->header;
        print qq(<!doctype html><html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="A layout example that shows off a responsive product landing page.">
    <title>Hi! | The Pirate Bay &#127988;&#8205;&#9760;&#65039;</title>
    <link rel="icon" type="image/x-icon" href="../img/favicon.ico" sizes="128x128">
    <link rel="stylesheet" href="../css/pure-min.css">
    <link rel="stylesheet" href="../css/grids-responsive-min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="stylesheet" href="../css/styles.css">
    <style>
        .center-screen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            min-height: 100vh;
        }

        .pure-button {
            font-family: inherit;
            font-size: 100%;
            padding: 0.5em 1em;
            color: white !important;
            border: none transparent;
            background-color: white;
            text-decoration: none;
            border-radius: 2px;
        }

        .pure-button-primary,
        .pure-button-selected,
        a.pure-button-primary,
        a.pure-button-selected {
            background-color: #1f8dd6;
            color: #fff;
        }
    </style>
</head>

<body>
    <div class="header">
        <div class="home-menu pure-menu pure-menu-horizontal pure-menu-fixed">
            <a class="pure-menu-heading" href="https://nonuser.onthewifi.com/">The Pirate Bay</a>

            <ul class="pure-menu-list">
                <li class="pure-menu-item pure-menu-selected"><a href="https://nonuser.onthewifi.com/" class="pure-menu-link">Inicio</a></li>
                <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/ayuda.html" class="pure-menu-link">Ayuda</a></li>
                <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/cgi-bin/login.cgi" class="pure-menu-link">Mi cuenta</a></li>
            </ul>
        </div>
    </div>
    <div class="content center-screen">
        <h2 class="content-head is-center">Acceso Restringido</h2>
        <h3 class="content-head is-center">Para volver al inicio pulse el botón inferior.</h3>

        <div class="pure-g">
            <div class="l-box-lrg pure-u-1 pure-u-md-2-5">
                <button onclick="location.href ='https://nonuser.onthewifi.com/';" method="Post" class="pure-button pure-button-primary">INICIO</button>
            </div>
        </div>
    </div>
    <div class="footer l-box is-center">Copyright © 2021, The Pirate Bay<br>All rights reserved.</div>
</body>

</html>);
    }
}