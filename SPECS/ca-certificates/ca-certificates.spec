Summary:	Certificate Authority certificates 
Name:		ca-certificates
Version:	20180919
Release:	1%{?dist}
License:	Custom
# http://anduin.linuxfromscratch.org/BLFS/other/certdata.txt
URL:            http://anduin.linuxfromscratch.org/BLFS/other/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	certdata.txt
Requires: 	openssl
BuildRequires:	openssl
Requires:       ca-certificates-pki = %{version}-%{release}
Requires(post): /bin/ln
Provides:       ca-certificates-mozilla
%description
The Public Key Inrastructure is used for many security issues in a
Linux system. In order for a certificate to be trusted, it must be
signed by a trusted agent called a Certificate Authority (CA). The
certificates loaded by this section are from the list on the Mozilla
version control system and formats it into a form used by 
OpenSSL-1.0.1e. The certificates can also be used by other applications
either directly of indirectly through openssl.
%package pki
Summary:  Certificate Authority certificates (pki tls certs)
Group:    System Environment/Security
%description pki
Certificate Authority certificates (pki tls certs)

%prep -p exit
%build
[ %{builddir} != "/"] && rm -rf %{builddir}/*
install -vdm 755 %{_builddir}/bin/
cp %{SOURCE0} %{_builddir}
#
#	make-cert.pl
#
cat > %{_builddir}/bin/make-cert.pl << "EOF"
#!/usr/bin/perl -w
# Used to generate PEM encoded files from Mozilla certdata.txt.
# Run as ./make-cert.pl > certificate.crt
# Parts of this script courtesy of RedHat (mkcabundle.pl)
# This script modified for use with single file data (tempfile.cer) extracted
# from certdata.txt, taken from the latest version in the Mozilla NSS source.
# mozilla/security/nss/lib/ckfw/builtins/certdata.txt
# Authors:	DJ Lucas
#		Bruce Dubbs
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
EOF
#
#	make-ca.sh
#
cat > %{_builddir}/bin/make-ca.sh << "EOF"
#!/bin/bash
# Begin make-ca.sh
# Script to populate OpenSSL's CApath from a bundle of PEM formatted CAs
# The file certdata.txt must exist in the local directory
# Version number is obtained from the version of the data.
# Authors: DJ Lucas
#          Bruce Dubbs
# Version 20120211
certdata="certdata.txt"
if [ ! -r $certdata ]; then
  echo "$certdata must be in the local directory"
  exit 1
fi
REVISION=$(grep CVS_ID $certdata | cut -f4 -d'$')
if [ -z "${REVISION}" ]; then
  echo "$certfile has no 'Revision' in CVS_ID"
  exit 1
fi
VERSION=$(echo $REVISION | cut -f2 -d" ")
TEMPDIR=$(mktemp -d)
TRUSTATTRIBUTES="CKA_TRUST_SERVER_AUTH"
BUNDLE="BLFS-ca-bundle-${VERSION}.crt"
CONVERTSCRIPT="bin/make-cert.pl"
SSLDIR="/etc/ssl"
mkdir "${TEMPDIR}/certs"
# Get a list of staring lines for each cert
CERTBEGINLIST=$(grep -n "^# Certificate" "${certdata}" | cut -d ":" -f1)
# Get a list of ending lines for each cert
CERTENDLIST=`grep -n "^CKA_TRUST_STEP_UP_APPROVED" "${certdata}" | cut -d ":" -f 1`
# Start a loop
for certbegin in ${CERTBEGINLIST}; do
  for certend in ${CERTENDLIST}; do
    if test "${certend}" -gt "${certbegin}"; then
      break
    fi
  done
  # Dump to a temp file with the name of the file as the beginning line number
  sed -n "${certbegin},${certend}p" "${certdata}" > "${TEMPDIR}/certs/${certbegin}.tmp"
done
unset CERTBEGINLIST CERTDATA CERTENDLIST certebegin certend
mkdir -p certs
rm certs/*      # Make sure the directory is clean
for tempfile in ${TEMPDIR}/certs/*.tmp; do
  # Make sure that the cert is trusted...
  grep "CKA_TRUST_SERVER_AUTH" "${tempfile}" | \
    egrep "TRUST_UNKNOWN|NOT_TRUSTED" > /dev/null
  if test "${?}" = "0"; then
    # Throw a meaningful error and remove the file
    cp "${tempfile}" tempfile.cer
    perl ${CONVERTSCRIPT} > tempfile.crt
    keyhash=$(openssl x509 -noout -in tempfile.crt -hash)
    echo "Certificate ${keyhash} is not trusted!  Removing..."
    rm -f tempfile.cer tempfile.crt "${tempfile}"
    continue
  fi
  # If execution made it to here in the loop, the temp cert is trusted
  # Find the cert data and generate a cert file for it
  cp "${tempfile}" tempfile.cer
  perl ${CONVERTSCRIPT} > tempfile.crt
  keyhash=$(openssl x509 -noout -in tempfile.crt -hash)
  mv tempfile.crt "certs/${keyhash}.pem"
  rm -f tempfile.cer "${tempfile}"
  echo "Created ${keyhash}.pem"
done
# Remove blacklisted files
# MD5 Collision Proof of Concept CA
if test -f certs/8f111d69.pem; then
  echo "Certificate 8f111d69 is not trusted!  Removing..."
  rm -f certs/8f111d69.pem
fi
# Finally, generate the bundle and clean up.
cat certs/*.pem >  ${BUNDLE}
rm -r "${TEMPDIR}"
EOF
#
#	remove-expired-certs.sh\
#
cat > %{_builddir}/bin/remove-expired-certs.sh << "EOF"
#!/bin/bash
# Begin /bin/remove-expired-certs.sh
# Version 20120211
# Make sure the date is parsed correctly on all systems
function mydate()
{
  local y=$( echo $1 | cut -d" " -f4 )
  local M=$( echo $1 | cut -d" " -f1 )
  local d=$( echo $1 | cut -d" " -f2 )
  local m
  if [ ${d} -lt 10 ]; then d="0${d}"; fi
  case $M in
    Jan) m="01";;
    Feb) m="02";;
    Mar) m="03";;
    Apr) m="04";;
    May) m="05";;
    Jun) m="06";;
    Jul) m="07";;
    Aug) m="08";;
    Sep) m="09";;
    Oct) m="10";;
    Nov) m="11";;
    Dec) m="12";;
  esac
  certdate="${y}${m}${d}"
}
OPENSSL=/usr/bin/openssl
DIR=certs
if [ $# -gt 0 ]; then
  DIR="$1"
fi
certs=$( find ${DIR} -type f -name "*.pem" -o -name "*.crt" )
today=$( date +%Y%m%d )
for cert in $certs; do
  notafter=$( $OPENSSL x509 -enddate -in "${cert}" -noout )
  date=$( echo ${notafter} |  sed 's/^notAfter=//' )
  mydate "$date"
  if [ ${certdate} -lt ${today} ]; then
     echo "${cert} expired on ${certdate}! Removing..."
     rm -f "${cert}"
  fi
done
EOF

chmod +x %{_builddir}/bin/make-cert.pl
chmod +x %{_builddir}/bin/make-ca.sh
chmod +x %{_builddir}/bin/remove-expired-certs.sh

printf "making certs\n"
bin/make-ca.sh
printf "Removing expired certs\n"
bin/remove-expired-certs.sh
printf "Build portion completed\n"

sed -i 's|CONVERTSCRIPT="bin/make-cert.pl"|CONVERTSCRIPT="/bin/make-cert.pl"|' bin/make-ca.sh
sed -i 's|DIR=certs|DIR=/etc/ssl/certs|' bin/remove-expired-certs.sh
%install
SSLDIR=/etc/ssl
install -d %{buildroot}/${SSLDIR}/certs
install -d %{buildroot}/etc/pki/tls/certs
cp -v certs/*.pem %{buildroot}/${SSLDIR}/certs
install BLFS-ca-bundle*.crt %{buildroot}/etc/pki/tls/certs/ca-bundle.crt
#ln -sfv ../$(readlink %{buildroot}/${SSLDIR}/ca-bundle.crt) %{buildroot}/${SSLDIR}/certs/ca-certificates.crt
unset SSLDIR

install -Dm644 bin/make-ca.sh %{buildroot}/bin/make-ca.sh
install -Dm644 bin/make-cert.pl %{buildroot}/bin/make-cert.pl
install -Dm644 bin/remove-expired-certs.sh %{buildroot}/bin/remove-expired-certs.sh
%{_fixperms} %{buildroot}/*
%post 
cd /etc/ssl/certs;
for file in *.pem; do ln -sf $file `openssl x509 -hash -noout -in $file`.0; done
exit 0
%clean
%files
%defattr(-,root,root)
/etc/ssl/certs/*
/bin/make-ca.sh
/bin/remove-expired-certs.sh
/bin/make-cert.pl
%files pki
%defattr(-,root,root)
/etc/pki/tls/certs/ca-bundle.crt
%changelog
*       Tue Sep 25 2018 Ankit Jain <ankitja@vmware.com> 20180919-1
-       Updating mozilla certdata.txt to latest rev. Also added -pki subpackage
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 20160109-5
-	GA - Bump release of all rpms
*	Wed Feb 10 2016 Anish Swaminathan <anishs@vmware.com> 20160109-4
-	Add Provides field
*	Mon Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 20160109-3
-	Force create links for certificates
*	Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 20160109-2
-	Remove c_rehash dependency
*       Wed Jan 13 2016 Divya Thaluru <dthaluru@vmware.com> 20160109-1
-       Updating mozilla certdata.txt to latest revision
*	Wed Oct 15 2014 Divya Thaluru <dthaluru@vmware.com> 20130524-1
-	Initial build.	First version
