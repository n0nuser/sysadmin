#!/usr/bin/perl -w

use warnings;
use utf8;

use CGI;
use CGI::Cookie;
use CGI::Session;

use Linux::usermod;
use File::Copy::Recursive;

use SQL::Abstract;
use DBI;

use Email::MIME;
use Email::Sender::Simple qw(sendmail);
use MIME::Words qw(:all);

$cgi = CGI->new;

# Valores pagina web
$username = lc($cgi->param('username'));
$password = $cgi->param('password1');
$email = $cgi->param('email');
$name = $cgi->param('name');
$surname = $cgi->param('surname');

# Base datos
$usuarioDB = "root";
$claveDB = "admin";
$DB = "usuarios";
$tabla = 'datos';

# Usuario Sistema
$directory = "/home/$username";
$group = "1001";
$shell = "/bin/bash";

# Creamos el objeto para SQL Abstract
my $sql = SQL::Abstract->new;

# Conectamos con la BD.
$dbh = DBI->connect("DBI:MariaDB:$DB:localhost", $usuarioDB, $claveDB) or print "\nError al abrir la base de datos.\n";

my %where = (email => $email);
my($stmt, @bind) = $sql->select($tabla,'usuario',\%where);
my $sth = $dbh->prepare($stmt);
$sth->execute(@bind);
$query = $sth->fetchrow_array;
if ($query eq "" ){

    # Datos usuarios
    my %data = (
        usuario => $username,
        nombre => $name,
        apellidos => $surname,
        email => $email,
    );

    # Genera Query para insertar
    my($stmt, @bind) = $sql->insert($tabla, \%data);

    # Ejecutar Query
    my $sth = $dbh->prepare($stmt);
    $sth->execute(@bind);

    # Desconectamos de la BD.
    $dbh->disconnect or warn "\nFallo al desconectar.\n";

    Linux::usermod->add($username, $password, '', $group, '', $directory, $shell);
    ($name, $pass, $uid, $gid, $quota, $comment, $gcos, $dir, $shell, $expire) = getpwnam($username);

    $chownFile="/var/www/nameNew/$username";
    open(FH, '>', $chownFile) or print "Failed to create empty: $!\n";
    close(FH);

    # Mandar correo
    $BODY = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html data-editor-version="2" class="sg-campaigns" xmlns="http://www.w3.org/1999/xhtml">

    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
    <!--[if !mso]><!-->
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <style type="text/css">
        body,
        p,
        div {
        font-family: inherit;
        font-size: 14px;
        }

        body {
        color: #000000;
        }

        body a {
        color: #1188E6;
        text-decoration: none;
        }

        p {
        margin: 0;
        padding: 0;
        }

        table.wrapper {
        width: 100% !important;
        table-layout: fixed;
        -webkit-font-smoothing: antialiased;
        -webkit-text-size-adjust: 100%;
        -moz-text-size-adjust: 100%;
        -ms-text-size-adjust: 100%;
        }

        img.max-width {
        max-width: 100% !important;
        }

        .column.of-2 {
        width: 50%;
        }

        .column.of-3 {
        width: 33.333%;
        }

        .column.of-4 {
        width: 25%;
        }

        @media screen and (max-width:480px) {

        .preheader .rightColumnContent,
        .footer .rightColumnContent {
            text-align: left !important;
        }

        .preheader .rightColumnContent div,
        .preheader .rightColumnContent span,
        .footer .rightColumnContent div,
        .footer .rightColumnContent span {
            text-align: left !important;
        }

        .preheader .rightColumnContent,
        .preheader .leftColumnContent {
            font-size: 80% !important;
            padding: 5px 0;
        }

        table.wrapper-mobile {
            width: 100% !important;
            table-layout: fixed;
        }

        img.max-width {
            height: auto !important;
            max-width: 100% !important;
        }

        a.bulletproof-button {
            display: block !important;
            width: auto !important;
            font-size: 80%;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        .columns {
            width: 100% !important;
        }

        .column {
            display: block !important;
            width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
        }
    </style>
    <link href="https://fonts.googleapis.com/css?family=Chivo&display=swap" rel="stylesheet">
    <style>
        body {
        font-family: "Chivo", sans-serif;
        }
    </style>
    <!--End Head user entered-->
    </head>

    <body>
    <center class="wrapper" data-link-color="#1188E6"
        data-body-style="font-size:14px; font-family:inherit; color:#000000; background-color:#FFFFFF;">
        <div class="webkit">
        <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
            <tbody>
            <tr>
                <td valign="top" bgcolor="#FFFFFF" width="100%">
                <table width="100%" role="content-container" class="outer" align="center" cellpadding="0" cellspacing="0"
                    border="0">
                    <tbody>
                    <tr>
                        <td width="100%">
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tbody>
                            <tr>
                                <td>
                                <!--[if mso]>
        <center>
        <table><tr><td width="600">
    <![endif]-->
                                <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                    style="width:100%; max-width:600px;" align="center">
                                    <tbody>
                                    <tr>
                                        <td role="modules-container"
                                        style="padding:0px 0px 0px 0px; color:#000000; text-align:left;" bgcolor="#FFFFFF"
                                        width="100%" align="left">
                                        <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%"
                                            role="module" data-type="columns" style="padding:30px 0px 30px 30px;"
                                            bgcolor="#00634a">
                                            <tbody>
                                            <tr role="module-content">
                                                <td height="100%" valign="top">
                                                <table class="column" width="570"
                                                    style="width:570px; border-spacing:0; border-collapse:collapse; margin:0px 0px 0px 0px;"
                                                    cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="">
                                                    <tbody>
                                                    <tr>
                                                        <td style="padding:0px;margin:0px;border-spacing:0;">
                                                        <table class="wrapper" role="module" data-type="image" border="0"
                                                            cellpadding="0" cellspacing="0" width="100%"
                                                            style="table-layout: fixed;"
                                                            data-muid="33d39ee4-da50-404a-8d62-ac83a12a2429">
                                                            <tbody>
                                                            <tr>
                                                                <td
                                                                style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;"
                                                                valign="top" align="left">
                                                                <p style="color:white;  font-family: " Lucida
                                                                    Sans", "Lucida Sans Regular" , "Lucida Grande"
                                                                    , "Lucida Sans Unicode" , Geneva, Verdana, sans-serif;">
                                                                    nonuser.onthewifi.com</p>
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%"
                                            role="module" data-type="columns" style="padding:50px 0px 0px 30px;"
                                            bgcolor="#fff7ea">
                                            <tbody>
                                            <tr role="module-content">
                                                <td height="100%" valign="top">
                                                <table class="column" width="550"
                                                    style="width:550px; border-spacing:0; border-collapse:collapse; margin:0px 10px 0px 10px;"
                                                    cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="">
                                                    <tbody>
                                                    <tr>
                                                        <td style="padding:0px;margin:0px;border-spacing:0;">
                                                        <table class="module" role="module" data-type="text" border="0"
                                                            cellpadding="0" cellspacing="0" width="100%"
                                                            style="table-layout: fixed;"
                                                            data-muid="b16a4afb-f245-4156-968e-8080176990ea"
                                                            data-mc-module-version="2019-10-22">
                                                            <tbody>
                                                            <tr>
                                                                <td
                                                                style="padding:18px 40px 0px 0px; line-height:22px; text-align:inherit;"
                                                                height="100%" valign="top" bgcolor=""
                                                                role="module-content">
                                                                <div>
                                                                    <div style="font-family: inherit; text-align: inherit">
                                                                    <span style="color: #00634a; font-size: 24px">¡Te has
                                                                        registrado correctamente!</span>
                                                                    </div>
                                                                    <div></div>
                                                                </div>
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                        <table class="module" role="module" data-type="text" border="0"
                                                            cellpadding="0" cellspacing="0" width="100%"
                                                            style="table-layout: fixed;"
                                                            data-muid="b16a4afb-f245-4156-968e-8080176990ea.1"
                                                            data-mc-module-version="2019-10-22">
                                                            <tbody>
                                                            <tr>
                                                                <td
                                                                style="padding:18px 40px 10px 0px; line-height:18px; text-align:inherit;"
                                                                height="100%" valign="top" bgcolor=""
                                                                role="module-content">
                                                                <div>
                                                                    <div style="font-family: inherit; text-align: inherit">
                                                                    <span style="color: #00634a"><strong>Los datos de
                                                                        registro son los siguientes:</strong></span>
                                                                    </div>
                                                                    <div style="font-family: inherit; text-align: inherit">
                                                                    <span style="color: #00634a"><br><strong>Usuario:
                                                                        </strong>' . $username . '<br><strong>Contraseña:
                                                                        </strong>' . $password . '<br><strong>Nombre:
                                                                        </strong>' . $name . '<br><strong>Apellidos:
                                                                        </strong>' . $surname . '&nbsp;</span>
                                                                    </div>
                                                                </div>
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                        <table class="module" role="module" data-type="spacer" border="0"
                                                            cellpadding="0" cellspacing="0" width="100%"
                                                            style="table-layout: fixed;"
                                                            data-muid="c97177b8-c172-4c4b-b5bd-7604cde23e3f">
                                                            <tbody>
                                                            <tr>
                                                                <td style="padding:0px 0px 10px 0px;" role="module-content"
                                                                bgcolor="">
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                        <table class="module" role="module" data-type="text" border="0"
                                                            cellpadding="0" cellspacing="0" width="100%"
                                                            style="table-layout: fixed;"
                                                            data-muid="b16a4afb-f245-4156-968e-8080176990ea.1.1"
                                                            data-mc-module-version="2019-10-22">
                                                            <tbody>
                                                            <tr>
                                                                <td
                                                                style="padding:18px 40px 10px 0px; line-height:18px; text-align:inherit;"
                                                                height="100%" valign="top" bgcolor=""
                                                                role="module-content">
                                                                <div>
                                                                    <div style="font-family: inherit; text-align: inherit">
                                                                    <span style="color: #00634a">Si usted no ha creado
                                                                        esta cuenta, por favor, contáctenos.</span>
                                                                    </div>
                                                                    <div style="font-family: inherit; text-align: inherit">
                                                                    <span style="color: #00634a"><br>
                                                                    </span>
                                                                    </div>
                                                                    <div style="font-family: inherit; text-align: inherit">
                                                                    <span style="color: #00634a">Mándenos un email a
                                                                        <a
                                                                        href="mailto:admin@nonuser.onthewifi.com">admin@nonuser.onthewifi.com&nbsp;</a></span>
                                                                    </div>
                                                                    <div></div>
                                                                </div>
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                        <table class="module" role="module" data-type="spacer" border="0"
                                                            cellpadding="0" cellspacing="0" width="100%"
                                                            style="table-layout: fixed;"
                                                            data-muid="c97177b8-c172-4c4b-b5bd-7604cde23e3f.1.1">
                                                            <tbody>
                                                            <tr>
                                                                <td style="padding:0px 0px 80px 0px;" role="module-content"
                                                                bgcolor="">
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                    </tbody>
                </table>
        </div>
    </center>
    </body>

    </html>';

    my $message = Email::MIME->create(
        header_str => [
            From    => '"The Pirate Bay" <admin@nonuser.onthewifi.com>',
            To      => $email,
            Subject => "¡Registrado satisfactoriamente!",
            Charset => 'utf-8',
            Encoding => 'B',
            'Content-Type' => 'text/html',
        ],
        attributes => {
            encoding => 'base64',
            charset  => 'UTF-8',
        },
        body_str => $BODY,
    );
    sendmail($message);

    # Se crea una nueva
    $session = CGI::Session->new();
    $session->save_param($cgi);
    $session->expires("+1h");
    $session->flush();
    print $session->header(-location => "dashboard.cgi");
}
else {
    # Desconectamos de la BD.
    $dbh->disconnect or warn "\nFallo al desconectar.\n";
    print $cgi->header;
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
    </head>

    <body>
        <div class="header">
            <div class="home-menu pure-menu pure-menu-horizontal pure-menu-fixed">
                <a class="pure-menu-heading" href="https://nonuser.onthewifi.com/">The Pirate Bay</a>

                <ul class="pure-menu-list">
                    <li class="pure-menu-item pure-menu-selected"><a href="https://nonuser.onthewifi.com/" class="pure-menu-link">Inicio</a></li>
                    <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/ayuda.html" class="pure-menu-link">Ayuda</a></li>
                    <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/cgi-bin/login.cgi" class="pure-menu-link">Iniciar sesión</a></li>
                </ul>
            </div>
        </div>
        <div class="content center-screen">
            <h2 class="content-head is-center">ERROR</h2>
            <h3 class="content-head is-center">Ya existe un usuario con ese correo</h3>
            <br>
            <h3 class="content-head is-center">Para volver a intentar registrarse pulse el botón inferior</h3>

            <div class="pure-g">
                <div class="l-box-lrg pure-u-1 pure-u-md-2-5">
                    <button onclick="location.href ='https://nonuser.onthewifi.com/cgi-bin/register.cgi';" method="Post" class="pure-button pure-button-primary">VOLVER</button>
                </div>
            </div>
        </div>
        <div class="footer l-box is-center">Copyright © 2021, The Pirate Bay<br>All rights reserved.</div>
    </body>

    </html>);
}