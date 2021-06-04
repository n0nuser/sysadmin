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

#Creamos una array para guardar los datos de sesión
my @autenticar = $session->param;

if (@autenticar eq 0 || $session->is_expired) {
  print $q->header;
  $session->delete();
  $session->flush();
  print qq(<!DOCTYPE html
  PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <link rel="stylesheet" href="../css/pure-min.css">
  <link rel="stylesheet" href="../css/grids-responsive-min.css">
  <link rel="stylesheet" href="../css/styles.css">
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
</head>

<body>
  <div class="header">
    <div class="home-menu pure-menu pure-menu-horizontal pure-menu-fixed">
      <a class="pure-menu-heading" href="https://nonuser.onthewifi.com/">The Pirate Bay</a>

      <ul class="pure-menu-list">
        <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/var/www/html/ayuda.html" class="pure-menu-link">Ayuda</a></li>
        <li class="pure-menu-item"><a href="#" class="pure-menu-link">Mi cuenta</a></li>
      </ul>
    </div>
  </div>
  <div class="center-screen">
    <form class="pure-form" action="/cgi-bin/logged.cgi" method="Post">
      <fieldset style="background: white; padding: 2em; border: 20px; border-radius: 15px; border-color: black;">
        <input name="email" type="text" placeholder="Email" /><br>
        <input name="password" type="password" placeholder="Password" /><br>
        <button type="submit" class="pure-button pure-button-primary">Iniciar Sesión</button>
        <p>¿No tienes cuenta? <a href="register.cgi">Regístrate</a></p>
        <p>¿Has olvidado tu contraseña? <a href="forgot.cgi">Contraseña olvidada</a></p>
      </fieldset>
    </form>
  </div>
</body>

</html>);
} else {
  print $q->redirect("https://nonuser.onthewifi.com/cgi-bin/dashboard.cgi");
}