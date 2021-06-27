#!/usr/bin/perl -wT

use warnings;
use CGI;
use CGI::Session;
use Filesys::DiskUsage qw/du/;
use Proc::ProcessTable;
use SQL::Abstract;
use DBI;
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
    # Base datos
    my $usuarioDB = "root";
    my $claveDB = "admin";
    my $DB = "usuarios";
    my $tabla = 'datos';

    # Uso de disco: diskUsage
    $diskUsage = "";
    $buffer = "";
    my $sql = SQL::Abstract->new;
    my $dbh = DBI->connect("DBI:MariaDB:$DB:localhost", $usuarioDB, $claveDB) or print "\nError al abrir la base de datos.\n";
    my($stmt, @bind) = $sql->select($tabla,'usuario');
    my $sth = $dbh->prepare($stmt);
    $sth->execute(@bind);
    my @usuarios;
    while (@usuarios = $sth->fetchrow_array){
        my $usuario = $usuarios[0];
        $diskUsage = "$diskUsage" . "Nombre del usuario: $usuario\n";
        my $dir = "/home/" . $usuario . "/";
        my $tam = du ( { 'human-readable' => 1 } , $dir );
        $buffer = sprintf( '%-20s %-20s' . "\n" . '%-20s %-20s' . "\n","Espacio usado","Directorio","$tam","$dir");
        $diskUsage = "$diskUsage" . "$buffer";
    }
    $dbh->disconnect or warn "\nFallo al desconectar.\n";
    
    # Info sobre procesos: procInfo
    $procInfo = "";
    my $t = new Proc::ProcessTable;
    my $p;
    my $linea;
    my $buffer = "";
    $buffer = sprintf( '%-6s %-10s %-10s %-10s %-50s' . "\n","PID","STAT","%MEM","CPU","COMMAND\n");  
    $procInfo = "$procInfo" . "$buffer";
    foreach $p ( @{$t->table} ){
        $buffer = sprintf( '%-6d %-10s %-10f %-10f %-50s' . "\n",$p->pid,$p->state,$p->pctmem,$p->pctcpu,$p->cmndline);
        $procInfo = "$procInfo" . "$buffer";
    }

    # Info sobre memoria: memInfo
    $memInfo = "";
    open(my $fh, '<', "/proc/meminfo");
    {
        local $/;
        $memInfo = <$fh>;
    }    
    close($fh);

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
    <link rel="icon" type="image/x-icon" href="../img/favicon.ico" sizes="128x128">
    <link rel="stylesheet" href="../css/pure-min.css">
    <link rel="stylesheet" href="../css/grids-responsive-min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="stylesheet" href="../css/styles.css">
    <style>
      .center-screen {
      display: block;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
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
      .pure-button-primary1,
      .pure-button-selected,
      a.pure-button-primary,
      a.pure-button-selected {
      background-color: #D22B2B;
      color: #fff;
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
    <div class="content">
      <br><br>
      <h2 class="content-head is-center">Bienvenido $username</h2>
      <div class="pure-g center-screen">
        <div class="l-box pure-u-1 pure-u-md-1-2 pure-u-lg-1-4">
          <form class="pure-form" action="/cgi-bin/deleteAdmin.cgi" method="Post">
            <fieldset style="background: white; padding: 2em; border: 20px; border-radius: 15px; border-color: black;">
              <input name="user" type="text" placeholder="Usuario" />
              <button type="submit" class="pure-button pure-button-primary1">Eliminar cuenta</button>
            </fieldset>
          </form>
        </div>
      </div>
      <div class="pure-g center-screen">
        <button onclick="location.href ='https://nonuser.onthewifi.com/cgi-bin/admin.cgi';" method="Post" class="pure-button pure-button-primary">Refrescar estadísticas de uso</button>
      </div>
      <div class="pure-g center-screen">  
        <div class="l-box pure-u-1 pure-u-md-1-2 pure-u-lg-1-4">
          <h3>Disk Usage per User</h3>
          <details>
          <summary>Open Here!</summary>
          <pre>$diskUsage</pre>
          </details>
        </div>
      
        <div class="l-box pure-u-1 pure-u-md-1-2 pure-u-lg-1-4">  
          <h3>Process Information</h3>
          <details>
          <summary>Open Here!</summary>
          <pre>$procInfo</pre>
          </details>
        </div>
        
        <div class="l-box pure-u-1 pure-u-md-1-2 pure-u-lg-1-4">
          <h3>Memory Information</h3>
          <details>
          <summary>Open Here!</summary>
          <pre>$memInfo</pre>
          </details>
        </div>
      </div>
    </div>
    <div class="footer l-box is-center">Copyright © 2021, The Pirate Bay<br>All rights reserved.</div>
  </body>
</html>
);
}