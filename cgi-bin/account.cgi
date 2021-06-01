#!/usr/bin/perl -w

use warnings;
use Linux::usermod;
use CGI;
use utf8;
use File::Copy::Recursive;

$q = CGI->new;
print $q->header;

print '<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="A layout example that shows off a responsive product landing page.">
    <title>Hi! | The Pirate Bay 🏴‍☠️</title>
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
    </style>
</head>

<body>
    <div class="header">
        <div class="home-menu pure-menu pure-menu-horizontal pure-menu-fixed">
            <a class="pure-menu-heading" href="index.html">The Pirate Bay</a>

            <ul class="pure-menu-list">
                <li class="pure-menu-item pure-menu-selected"><a href="#" class="pure-menu-link">Inicio</a></li>
                <li class="pure-menu-item"><a href="#" class="pure-menu-link">Ayuda</a></li>
                <li class="pure-menu-item"><a href="account.html" class="pure-menu-link">Mi cuenta</a></li>
            </ul>
        </div>
    </div>
    <div class="content center-screen">
        <h2 class="content-head is-center">¡Hola usuario!</h2>

        <div class="pure-g">
            <div class="l-box-lrg pure-u-1 pure-u-md-2-5">
                <form class="pure-form pure-form-stacked">
                    <fieldset>
                        <label for="name">Modificar mis datos</label>
                        <button type="submit" class="pure-button pure-button-primary">Modificar</button>
                        <br>
                        <label for="email">Cambiar contraseña</label>
                        <button type="submit" class="pure-button pure-button-primary">Cambiar contraseña</button>
                        <br>
                        <label for="email">Eliminar cuenta</label>
                        <button type="submit" class="pure-button pure-button-primary1">Eliminar</button>
                    </fieldset>
                </form>
            </div>
        </div>
    </div>
    <div class="footer l-box is-center">Copyright © 2021, The Pirate Bay<br>All rights reserved.</div>
</body>

</html>'