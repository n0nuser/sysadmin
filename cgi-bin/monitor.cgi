#!/usr/bin/perl -w
use Sys::Load qw/getload uptime/;

# Load
print "System load: ", (getload())[0], "<br>";
print "System uptime: ", int uptime(), "<br>";