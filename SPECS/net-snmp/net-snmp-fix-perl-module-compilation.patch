From: Bart Van Assche <bvanassche@acm.org>
Date: Sun, 24 Jul 2016 18:58:18 -0800
Subject: Fix Perl module compilation

Avoid that building the Net-SNMP Perl modules fails as follows:
ERROR from evaluation of /sources/net-snmp-5.7.3/perl/ASN/Makefile.PL:Bizarre
copy of HASH in list assignment at /usr/lib/perl5/site_perl/5.24.0/Carp.pm line 229.
--- a/perl/ASN/Makefile.PL
+++ b/perl/ASN/Makefile.PL
@@ -7,9 +7,7 @@
 # See lib/ExtUtils/MakeMaker.pm for details of how to influence
 # the contents of the Makefile that is written.
 
-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+WriteMakefile(InitMakeParams());
 
 Check_Version();

--- a/perl/Makefile.PL
+++ b/perl/Makefile.PL
@@ -3,9 +3,7 @@
 use Getopt::Long;
 require 5;

-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+WriteMakefile(InitMakeParams());

 sub InitMakeParams {
     $nsconfig="net-snmp-config"; # in path by default
--- a/perl/OID/Makefile.PL
+++ b/perl/OID/Makefile.PL
@@ -6,11 +6,8 @@
 use Config;
 use Getopt::Long;
 my $lib_version;
-my %MakeParams = ();
-
-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+
+WriteMakefile(InitMakeParams());
 
 Check_Version();

--- a/perl/SNMP/Makefile.PL
+++ b/perl/SNMP/Makefile.PL
@@ -3,15 +3,12 @@
 use Config;
 use Getopt::Long;
 my $lib_version;
-my %MakeParams = ();
 my $opts;
 
 # See lib/ExtUtils/MakeMaker.pm for details of how to influence
 # the contents of the Makefile that is written.
 
-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+WriteMakefile(InitMakeParams());
 
 Check_Version();

--- a/perl/TrapReceiver/Makefile.PL
+++ b/perl/TrapReceiver/Makefile.PL
@@ -3,11 +3,8 @@
 use Config;
 use Getopt::Long;
 my $lib_version;
-my %MakeParams = ();
-
-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+
+WriteMakefile(InitMakeParams());
 
 Check_Version();

--- a/perl/agent/Makefile.PL
+++ b/perl/agent/Makefile.PL
@@ -3,11 +3,8 @@
 use Config;
 use Getopt::Long;
 my $lib_version;
-my %MakeParams = ();
-
-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+
+WriteMakefile(InitMakeParams());
 
 Check_Version();

--- a/perl/agent/Support/Makefile.PL
+++ b/perl/agent/Support/Makefile.PL
@@ -3,14 +3,11 @@
 use Config;
 use Getopt::Long;
 my $lib_version;
-my %MakeParams = ();
 
 # See lib/ExtUtils/MakeMaker.pm for details of how to influence
 # the contents of the Makefile that is written.
 
-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+WriteMakefile(InitMakeParams());
 
 Check_Version();

--- a/perl/agent/default_store/Makefile.PL
+++ b/perl/agent/default_store/Makefile.PL
@@ -3,11 +3,8 @@
 use Config;
 use Getopt::Long;
 my $lib_version;
-my %MakeParams = ();
-
-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+
+WriteMakefile(InitMakeParams());
 
 Check_Version();

--- a/perl/default_store/Makefile.PL
+++ b/perl/default_store/Makefile.PL
@@ -3,11 +3,8 @@
 use Config;
 use Getopt::Long;
 my $lib_version;
-my %MakeParams = ();
 
-%MakeParams = InitMakeParams();
-
-WriteMakefile(%MakeParams);
+WriteMakefile(InitMakeParams());
 
 
 sub InitMakeParams {
