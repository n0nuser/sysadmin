#!/usr/bin/perl -w

use warnings;
use CGI;
use CGI::Session;
use utf8;
use SQL::Abstract;
use DBI;

$q = CGI->new;

# Gestión sesión
my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;

$usuarioDB = "root";
$claveDB = "admin";
$DB = "usuarios";
$tabla = 'datos';

if (@autenticar eq 0) {
    $session->delete();
    $session->flush();
    print $q->redirect("https://nonuser.onthewifi.com/");
} elsif ($session->is_expired) {
    $session->delete();
    $session->flush();
    print $q->redirect("https://nonuser.onthewifi.com/");
} else {
    print $q->header;
    my $username = $session->param("username");
    
    # Gestión base datos
    my $sql = SQL::Abstract->new();
    $dbh = DBI->connect("DBI:MariaDB:$DB:localhost", $usuarioDB, $claveDB) or print "\nError al abrir la base de datos.\n";
    my %where = (usuario => $username);
    my($stmt, @bind) = $sql->select($tabla,'email,nombre,apellidos',\%where);
    my $sth = $dbh->prepare($stmt);
    $sth->execute(@bind);
    @datos = $sth->fetchrow_array;
    $dbh->disconnect or warn "\nFallo al desconectar.\n";


    print qq(<!DOCTYPE html
            PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link rel="icon" type="image/x-icon" href="../img/favicon.ico" sizes="128x128">
        <link rel="stylesheet" href="../css/pure-min.css" />
        <link rel="stylesheet" href="../css/styles.css" />
        <link rel="stylesheet" href="../css/grids-responsive-min.css">
        <title>Login | The Pirate Bay &#127988;&#8205;&#9760;&#65039;</title>
        <style>
            .center-screen {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                min-height: 100vh;
            }

            body {
                background: url("../img/login.jpg") no-repeat center center fixed;
                -webkit-background-size: cover;
                -moz-background-size: cover;
                -o-background-size: cover;
                background-size: cover;
            }
        </style>
        <script>
            function forceLower(strInput) 
            {
            strInput.value=strInput.value.toLowerCase();
            }
        </script>​
    </head>

    <body>
        <div class="header">
            <div class="home-menu pure-menu pure-menu-horizontal pure-menu-fixed">
                <a class="pure-menu-heading" href="https://nonuser.onthewifi.com/">The Pirate Bay</a>
                <ul class="pure-menu-list">
                    <li class="pure-menu-item"><a href="dashboard.cgi" class="pure-menu-link">Dashboard</a></li>
                    <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/ayuda.html" class="pure-menu-link">Ayuda</a></li>
                    <li class="pure-menu-item"><a href="delSession.cgi" class="pure-menu-link">Cerrar Sesión</a></li>
                </ul>
            </div>
        </div>
        <div class="center-screen">
            <form class="pure-form" action="/cgi-bin/modified.cgi" method="Post">
                <fieldset style="background: white; padding: 2em; border: 20px; border-radius: 15px; border-color: black; text-align: left;">               
                    
                    <div class="pure-control-group">
                        <label for="aligned-email">Dirección de correo</label>
                        <input name="email" type="email" id="aligned-email" value="$datos[0]" required="required" placeholder="Introduzca su dirección de correo" />
                    </div>
                    <div class="pure-control-group">
                        <label for="aligned-foo">Nombre</label>
                        <input name="name" type="text" id="aligned-foo" value="$datos[1]" required="required" placeholder="Introduzca su nombre aquí" />
                    </div>
                    <div class="pure-control-group">
                        <label for="aligned-foo">Apellidos</label>
                        <input name="surname" type="text" id="aligned-foo" value="$datos[2]" required="required" placeholder="Introduzca sus apellidos aquí" />
                    </div>
                    <br />
                    <button type="submit" class="pure-button pure-button-primary">Modificar</button>
                </fieldset>
            </form>
        </div>
    </body>

    </html>);
}