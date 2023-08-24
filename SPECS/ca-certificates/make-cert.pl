#!/usr/bin/perl -w

# Used to generate PEM encoded files from Mozilla certdata.txt.
# Run as ./make-cert.pl > certificate.crt
# Parts of this script courtesy of RedHat (mkcabundle.pl)
# This script modified for use with single file data (tempfile.cer) extracted
# from certdata.txt, taken from the latest version in the Mozilla NSS source.
# mozilla/security/nss/lib/ckfw/builtins/certdata.txt
# Authors:  DJ Lucas
#   Bruce Dubbs
# Version 20120211

my $certdata = './tempfile.cer';

open( IN, "cat $certdata|" )
    || die "could not open $certdata";

my $incert = 0;
while ( <IN> )
{
    if ( /^CKA_VALUE MULTILINE_OCTAL/ )
    {
        $incert = 1;
        open( OUT, "|openssl x509 -text -inform DER -fingerprint" )
            || die "could not pipe to openssl x509";
    }
    elsif ( /^END/ && $incert )
    {
        close( OUT );
        $incert = 0;
        print "\n\n";
    }
    elsif ($incert)
    {
        my @bs = split( /\\/ );
        foreach my $b (@bs)
        {
            chomp $b;
            printf( OUT "%c", oct($b) ) unless $b eq '';
        }
    }
}
