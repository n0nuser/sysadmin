#!/usr/bin/perl -w

# CAVEATS
#   * Requires Authen::PAM module, which may also
#     require the pam-devel package.
#   * May need to be run as root in order to
#     access username/password file.

use CGI;
use CGI::Session;
use Authen::PAM;
use POSIX;
use utf8;

$cgi = CGI->new;
$username = $cgi->param(-name => 'username',-value => $cgi->param('email'));
$password = $cgi->param(-name => 'password',-value => $cgi->param('password'));
$service = "passwd";

# This "conversation function" will pass
# $password to PAM when it asks for it.
sub my_conv_func {
        my @res;
        while ( @_ ) {
                my $code = shift;
                my $msg = shift;
                my $ans = "";

                $ans = $username if ($code == PAM_PROMPT_ECHO_ON() );
                $ans = $password if ($code == PAM_PROMPT_ECHO_OFF() );

                push @res, (PAM_SUCCESS(),$ans);
        }
        push @res, PAM_SUCCESS();
        return @res;
}

# Initialize PAM object
if (!ref($pamh = new Authen::PAM($service, $username, \&my_conv_func))) {
    print "Authen::PAM init failed\n";
    exit 1;
}

# Authenticate with PAM
my $res = $pamh->pam_authenticate;

# Return success or failure
if ($res == PAM_SUCCESS()) {
    if ($username eq "admin")
    {
        my $session = new CGI::Session;
        $session->save_param($cgi);
        $session->expires("+1h");
        $session->flush();
        print $session->header(-location => "admin.cgi");
    }
    else{
        # https://www.youtube.com/watch?v=qtRRXy2oNUQ
        my $session = new CGI::Session;
        $session->save_param($cgi);
        $session->expires("+1h");
        $session->flush();
        print $session->header(-location => "dashboard.cgi");
    }
} else {
    print $cgi->redirect("https://nonuser.onthewifi.com/cgi-bin/login.cgi");
}