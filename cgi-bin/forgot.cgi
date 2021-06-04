#!/usr/bin/perl -w

use warnings;
use CGI;
use utf8;

$q = CGI->new;
print $q->header;

print qq(<!DOCTYPE html
          PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
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
                <li class="pure-menu-item pure-menu-selected">
                    <a href="https://nonuser.onthewifi.com/" class="pure-menu-link">Inicio</a>
                </li>
                <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/ayuda.html" class="pure-menu-link">Ayuda</a></li>
                <li class="pure-menu-item"><a href="login.cgi" class="pure-menu-link">Iniciar sesión</a></li>
            </ul>
        </div>
    </div>
    <div class="center-screen">
        <form class="pure-form" action="/cgi-bin/forgotten.cgi" method="Post">
            <fieldset style="background: white; padding: 2em; border: 20px; border-radius: 15px; border-color: black; text-align: left;">
                <div class="pure-control-group">
                    <label for="aligned-email">Dirección de correo</label>
                    <input name="email" type="email" id="aligned-email" placeholder="Introduzca su dirección de correo" />
                </div>                
                <br/>
                <button type="submit" class="pure-button pure-button-primary">Enviar</button>
            </fieldset>
        </form>
    </div>
</body>

</html>);