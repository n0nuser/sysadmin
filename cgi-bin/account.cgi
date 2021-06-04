#!/usr/bin/perl -wT

use warnings;
use CGI;
use CGI::Session;
use CGI::Cookie;
use utf8;

$q = CGI->new;

# Gestión sesión
my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;

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
print qq(<!doctype html><html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="A layout example that shows off a responsive product landing page.">
    <title>Hi! | The Pirate Bay &#127988;&#8205;&#9760;&#65039;</title>
    <link rel="stylesheet" href="../css/pure-min.css">
    <link rel="stylesheet" href="../css/grids-responsive-min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css">
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

        .pure-button-primary1,
        .pure-button-selected,
        a.pure-button-primary,
        a.pure-button-selected {
            background-color: #D22B2B;
            color: #fff;
        }
        .wrapper {
            display: grid;
            grid-gap: 30px;
            grid-template-columns: auto;
        }
        .wrapper_item {
            position: relative;
        }
    </style>
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
    <div class="content center-screen">
            <div class="l-box-lrg pure-u-1 pure-g wrapper">
                <label for="name">Modificar mis datos</label>
                <div class="wrapper_item">
                <button onclick="location.href ='/cgi-bin/modify.cgi';" method="Post"  class="pure-button pure-button-primary">Modificar</button>
                </div>

                <label for="email">Cambiar contraseña</label>
                <div class="wrapper_item">
                <button onclick="location.href ='/cgi-bin/password.cgi';" method="Post" class="pure-button pure-button-primary">Cambiar contraseña</button>
                </div>

                <label for="email">Eliminar cuenta</label>
                <div class="wrapper_item">
                <button onclick="location.href ='/cgi-bin/delete.cgi';" method="Post" class="pure-button pure-button-primary1">Eliminar</button>
                </div>
            </div>
    </div>
    <div class="footer l-box is-center">Copyright © 2021, The Pirate Bay<br>All rights reserved.</div>
</body>

</html>);
}