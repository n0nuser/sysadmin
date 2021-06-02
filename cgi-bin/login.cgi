#!/usr/bin/perl -w

# CAVEATS
#   * Requires Authen::PAM module, which may also
#     require the pam-devel package.
#   * May need to be run as root in order to
#     access username/password file.

use CGI;
use CGI::Cookie;
use Authen::PAM;
use POSIX;
use utf8;
use IPC::System::Simple qw(system capture);

$q = CGI->new;
$username = $q->param('email');
$password = $q->param('password');
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
    my $cookie = $q->cookie( -name => "campurriana", -value => $username, -path => "/" );
    
    if ($username eq "admin")
    {
        print $q->redirect ( -url => "https://nonuser.onthewifi.com/cgi-bin/admin.cgi", -cookie => $cookie );
    }
    else{
        print $q->redirect ( -url => "https://nonuser.onthewifi.com/cgi-bin/dashboard.cgi", -cookie => $cookie );
    }
} else {
    print $q->redirect("https://nonuser.onthewifi.com/login.html");
}