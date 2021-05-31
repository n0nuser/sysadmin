#!/usr/bin/perl -w

# CAVEATS
#   * Requires Authen::PAM module, which may also
#     require the pam-devel package.
#   * May need to be run as root in order to
#     access username/password file.

use CGI;
use Authen::PAM;
use POSIX;
use IPC::System::Simple qw(system capture);

$q = CGI->new;
$username = $q->param('email');
$password = $q->param('password');
$service = "passwd";

print $q->header;

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
    my $results = do {
        local $ENV{QUERY_STRING} = 'BARE=1';
        qx{./monitor.cgi};
    };
    print $results;
    #print $q->redirect("https://google.com");
} else {
    #print $q->redirect("https://apple.com");
    print "User or password wrong\n";
}