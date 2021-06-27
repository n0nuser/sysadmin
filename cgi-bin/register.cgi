#!/usr/bin/perl -w

use warnings;
use CGI;
use utf8;

$q = CGI->new;
print $q->header;

print qq(<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="../img/favicon.ico" sizes="128x128">
    <link rel="stylesheet" href="../css/pure-min.css" />
    <link rel="stylesheet" href="../css/styles.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
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
                <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/ayuda.html" class="pure-menu-link">Ayuda</a></li>
                <li class="pure-menu-item"><a href="login.cgi" class="pure-menu-link">Mi Cuenta</a></li>
            </ul>
        </div>
    </div>
    <div class="center-screen">
        <form class="pure-form" action="/cgi-bin/registered.cgi" method="Post">
            <fieldset style="background: white; padding: 2em; border: 20px; border-radius: 15px; border-color: black; text-align: left;">
                <div class="pure-control-group">
                    <label for="aligned-name">Nombre de usuario</label>
                    <input name="username" required="required" type="text" id="aligned-name" onkeyup="return forceLower(this);" placeholder="Introduzca su nombre de usuario" />
                </div>
                <div class="pure-control-group">
                    <label for="aligned-password">Contraseña</label>
                    <input name="password1" required="required" type="password" id="aligned-password" placeholder="Introduzca una contraseña" />
                </div>
                <div class="pure-control-group">
                    <label for="aligned-password">Confirmación de constraseña</label>
                    <input name="password2" type="password" id="aligned-password" placeholder="Confirmación de contraseña" />
                </div>
                <div class="pure-control-group">
                    <label for="aligned-email">Dirección de correo</label>
                    <input name="email" required="required" type="email" id="aligned-email" placeholder="Introduzca su dirección de correo" />
                </div>
                <div class="pure-control-group">
                    <label for="aligned-foo">Nombre</label>
                    <input name="name" required="required" type="text" id="aligned-foo" placeholder="Introduzca su nombre aquí" />
                </div>
                <div class="pure-control-group">
                    <label for="aligned-foo">Apellidos</label>
                    <input name="surname" required="required" type="text" id="aligned-foo" placeholder="Introduzca sus apellidos aquí" />
                </div>
                <br />
                <button type="submit" class="pure-button pure-button-primary">Registrarse</button>
            </fieldset>
        </form>
    </div>
</body>

</html>);