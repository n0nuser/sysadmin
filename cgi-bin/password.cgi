#!/usr/bin/perl -w

use warnings;
use Linux::usermod;
use CGI;
use CGI::Cookie;
use utf8;
use File::Copy::Recursive;

$q = CGI->new;

print $q->header;

%cookies = CGI::Cookie->fetch;
$username = $cookies{'campurriana'}->value;

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
    </style>
    <script>  
        function checkPassword(form) {
            password1 = form.password1.value;
            password2 = form.password2.value;

            if (password1 == '')
                alert ("Introduzca la contraseña");
                    
            else if (password2 == '')
                alert ("Introduzca la confirmación de contraseña");
                    
            else if (password1 != password2) {
                alert ("\nLas contraseñas no coinciden: Inténtelo de nuevo...")
                return false;
            }

            else{
                alert ("\nContraseña modificada correctamente.")
                return true;
            }
        }
    </script>
</head>

<body>
    <div class="header">
        <div class="home-menu pure-menu pure-menu-horizontal pure-menu-fixed">
            <a class="pure-menu-heading" href="https://nonuser.onthewifi.com/">The Pirate Bay</a>

            <ul class="pure-menu-list">
                <li class="pure-menu-item pure-menu-selected"><a href="https://nonuser.onthewifi.com/" class="pure-menu-link">Inicio</a></li>
                <li class="pure-menu-item"><a href="#" class="pure-menu-link">Ayuda</a></li>
                <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/login.html" class="pure-menu-link">Iniciar sesión</a></li>
            </ul>
        </div>
    </div>
    <div class="content center-screen">
        <form class="pure-form" onSubmit="return checkPassword(this)" action="/cgi-bin/passwd.cgi" method="Post">
            <fieldset style="background: white; padding: 2em; border: 20px; border-radius: 15px; border-color: black;">
                <input name="password1" type="password" placeholder="Contraseña nueva" /><br>
                <input name="password2" type="password" placeholder="Confirmar contraseña" /><br>
                <button type="submit" class="pure-button pure-button-primary">Modificar contraseña</button>
            </fieldset>
        </form>
    </div>
    <div class="footer l-box is-center">Copyright © 2021, The Pirate Bay<br>All rights reserved.</div>
</body>

</html>);