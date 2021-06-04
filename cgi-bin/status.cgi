#!/usr/bin/perl -w
use warnings;
use CGI;
use File::Slurp;
use Data::Dumper::Simple;
use strict;

my $q = CGI->new;

my $apache = read_file('/var/www/status/apache2');
my $sshd = read_file('/var/www/status/sshd');
my $postfix = read_file('/var/www/status/postfix');
my $dovecot = read_file('/var/www/status/dovecot');
my $mariadb = read_file('/var/www/status/mariadb');

my @services = ($apache, $sshd, $postfix, $dovecot, $mariadb);
my @servicios = ("apache2", "sshd", "postfix", "dovecot", "mariadb");
my $i = 5;

print $q->header;

print qq(<!doctype html>
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
                <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/ayuda.html" class="pure-menu-link">Ayuda</a></li>
                <li class="pure-menu-item"><a href="https://nonuser.onthewifi.com/cgi-bin/login.cgi"
                        class="pure-menu-link">Iniciar sesión</a></li>
            </ul>
        </div>
    </div>
    <div class="content center-screen">
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>
<script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
<!------ Include the above in your HEAD tag ---------->

<link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
<link href="//bootswatch.com/yeti/bootstrap.min.css" rel="stylesheet" type="text/css" />

<script src="//code.jquery.com/jquery.min.js"></script>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
  
  
  <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1>Status Page</h1>
        </div>
      </div>
      <div class="row clearfix">
          <div class="col-md-12 column">
              <div class="row clearfix">
                  <div class="col-md-12 column">
                      <div class="list-group">
                        );
                        for ($i = 0; $i < @services; $i++){
                            my $servicio = $servicios[$i];
                            my $label = 'label-success';
                            my $label2 = 'Operational';
                            if ($services[$i] != 1){
                                $label = 'label-danger';
                                $label2 = 'Not Operational';
                            }
                            print qq(
                          <div class="list-group-item">
                              <h4 class="list-group-item-heading">
                                  $servicio service
                                  <a href="#"  data-toggle="tooltip" data-placement="bottom" title="$servicio">
                                    <i class="fa fa-question-circle"></i>
                                  </a>
                              </h4>
                              <p class="list-group-item-text">
                                  <span class="label $label">$label2</span>
                              </p>
                          </div>
                            );
                        }
                        print qq(
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
    </div>
    <div class="footer l-box is-center">Copyright © 2021, The Pirate Bay<br>All rights reserved.</div>
</body>

</html>);