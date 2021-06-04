#!/usr/bin/perl -wT

use warnings;
use CGI;
use CGI::Cookie;
use CGI::Session;
use utf8;

$q = CGI->new;

#Crear un objeto CGI
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
    print qq(
<!doctype html>
<html lang="en">
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
          <li class="pure-menu-item"><a href="account.cgi" class="pure-menu-link">Ajustes</a></li>
          <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/ayuda.html" class="pure-menu-link">Ayuda</a></li>
          <li class="pure-menu-item"><a href="delSession.cgi" class="pure-menu-link">Cerrar Sesión</a></li>
        </ul>
      </div>
    </div>
    <div class="center-screen">
      <div class="content">
        <h2 class="content-head is-center">Bienvenido $username</h2>
        <div class="pure-g">
          <div class="l-box pure-u-1 pure-u-md-1-2 pure-u-lg-1-4">
            <h3 class="content-subhead">
              <i class="fa fa-rocket"></i>
              Servidor de correos
            </h3>
            <p>Accede a tu correo de forma fácil y rápida</p>
            <p><a href="https://nonuser.onthewifi.com/webmail/"
              class="pure-button pure-button-primary">Continuar</a></p>
          </div>
          <div class="l-box pure-u-1 pure-u-md-1-2 pure-u-lg-1-4">
            <h3 class="content-subhead">
              <i class="fa fa-mobile"></i>
              Almacenamiento para Webs
            </h3>
            <p>Crea un espacio para tu web (Almacenamiento 5MB)</p>
            <p>Conéctate mediante SFTP con el siguiente comando:</p>
            <pre>sftp -P 2222 $username\@nonuser.onthewifi.com</pre>
          </div>
          <div class="l-box pure-u-1 pure-u-md-1-2 pure-u-lg-1-4">
            <h3 class="content-subhead">
              <i class="fa fa-th-large"></i>
              Creación de Blogs con Hugo
            </h3>
            <p>Crea tus blogs personalizados y de forma rápida con GoHugo</p>
            <p><a href="" class="pure-button pure-button-primary">Crear</a></p>
          </div>
          <div class="l-box pure-u-1 pure-u-md-1-2 pure-u-lg-1-4">
            <h3 class="content-subhead">
              <i class="fas fa-phone-alt"></i>
              Servicio de VOIP
            </h3>
            <p>Hable con sus amigos fácilmente con nuestro servicio de voz.</p>
            <p><a href="" class="pure-button pure-button-primary">Continuar</a></p>
          </div>
        </div>
      </div>
    </div>
    <div class="footer l-box is-center">Copyright © 2021, The Pirate Bay<br>All rights reserved.</div>
  </body>
</html>
);
}