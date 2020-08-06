Summary:             Certificate Authority certificates for nxtgn openssl
Name:                ca-certificates-nxtgn-openssl
Version:             20200811
Release:             1%{?dist}
License:             Custom
URL:                 http://anduin.linuxfromscratch.org/BLFS/other/
Group:               System Environment/Security
Vendor:              VMware, Inc.
Distribution:        Photon
Source0:             certdata-nxtgn-openssl.txt
Requires:            nxtgn-openssl
BuildRequires:       nxtgn-openssl
Requires:            ca-certificates-nxtgn-openssl-pki = %{version}-%{release}
Requires(posttrans): /bin/ln
Provides:            ca-certificates-mozilla-nxtgn
%description
The Public Key Inrastructure is used for many security issues in a
Linux system. In order for a certificate to be trusted, it must be
signed by a trusted agent called a Certificate Authority (CA). The
certificates are generated using nxtgn openssl

%package pki
Summary:  Certificate Authority certificates (pki nxtgn openssl tls certs)
Group:    System Environment/Security

%description pki
Certificate Authority certificates (pki nxtgn openssl tls certs)

%prep -p exit
%build
[ %{builddir} != "/"] && rm -rf %{builddir}/*
install -vdm 755 %{_builddir}/bin/
cp %{SOURCE0} %{_builddir}
#
# make-nxtgn-cert.pl
#
cat > %{_builddir}/bin/make-nxtgn-cert.pl << "EOF"
#!/usr/bin/perl -w
# Used to generate PEM encoded files from Mozilla certdata-nxtgn-openssl.txt.
# Run as ./make-nxtgn-cert.pl > certificate.crt
# Parts of this script courtesy of RedHat (mkcabundle.pl)
# This script modified for use with single file data (tempfile.cer) extracted
# from certdata-nxtgn-openssl.txt, taken from the latest version in the Mozilla NSS source.
# mozilla/security/nss/lib/ckfw/builtins/certdata-nxtgn-openssl.txt
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
        open( OUT, "|nxtgn-openssl x509 -text -inform DER -fingerprint" )
            || die "could not pipe to nxtgn-openssl x509";
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
# make-nxtgn-ca.sh
#
cat > %{_builddir}/bin/make-nxtgn-ca.sh << "EOF"
#!/bin/bash
# Begin make-nxtgn-ca.sh
# Script to populate OpenSSL's CApath from a bundle of PEM formatted CAs
# The file certdata-nxtgn-openssl.txt must exist in the local directory
# Version number is obtained from the version of the data.
# Authors: DJ Lucas
#          Bruce Dubbs
# Version 20120211
certdata="certdata-nxtgn-openssl.txt"
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
CONVERTSCRIPT="bin/make-nxtgn-cert.pl"
SSLDIR="/etc/nxtgn-openssl"
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
    keyhash=$(nxtgn-openssl x509 -noout -in tempfile.crt -hash)
    echo "Certificate ${keyhash} is not trusted!  Removing..."
    rm -f tempfile.cer tempfile.crt "${tempfile}"
    continue
  fi
  # If execution made it to here in the loop, the temp cert is trusted
  # Find the cert data and generate a cert file for it
  cp "${tempfile}" tempfile.cer
  perl ${CONVERTSCRIPT} > tempfile.crt
  keyhash=$(nxtgn-openssl x509 -noout -in tempfile.crt -hash)
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
# remove-nxtgn-expired-certs.sh\
#
cat > %{_builddir}/bin/remove-nxtgn-expired-certs.sh << "EOF"
#!/bin/bash
# Begin /bin/remove-nxtgn-expired-certs.sh
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
OPENSSL=/usr/bin/nxtgn-openssl
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

chmod +x %{_builddir}/bin/make-nxtgn-cert.pl
chmod +x %{_builddir}/bin/make-nxtgn-ca.sh
chmod +x %{_builddir}/bin/remove-nxtgn-expired-certs.sh

printf "making certs\n"
bin/make-nxtgn-ca.sh
printf "Removing expired certs\n"
bin/remove-nxtgn-expired-certs.sh
printf "Build portion completed\n"

sed -i 's|CONVERTSCRIPT="bin/make-nxtgn-cert.pl"|CONVERTSCRIPT="/bin/make-nxtgn-cert.pl"|' bin/make-nxtgn-ca.sh
sed -i 's|DIR=certs|DIR=/etc/nxtgn-openssl/certs|' bin/remove-nxtgn-expired-certs.sh

%install
SSLDIR=/etc/nxtgn-openssl
install -d %{buildroot}/${SSLDIR}/certs
install -d %{buildroot}/etc/pki/tls/certs
cp -v certs/*.pem %{buildroot}/${SSLDIR}/certs
install BLFS-ca-bundle*.crt %{buildroot}/etc/pki/tls/certs/ca-bundle-nxtgn-openssl.crt
unset SSLDIR
install -Dm644 bin/make-nxtgn-ca.sh %{buildroot}/bin/make-nxtgn-ca.sh
install -Dm644 bin/make-nxtgn-cert.pl %{buildroot}/bin/make-nxtgn-cert.pl
install -Dm644 bin/remove-nxtgn-expired-certs.sh %{buildroot}/bin/remove-nxtgn-expired-certs.sh
%{_fixperms} %{buildroot}/*

%posttrans
cd /etc/nxtgn-openssl/certs;
for file in *.pem; do ln -sf $file `nxtgn-openssl x509 -hash -noout -in $file`.0; done
exit 0

%clean

%files
%defattr(-,root,root)
/etc/nxtgn-openssl/certs/*
/bin/make-nxtgn-ca.sh
/bin/remove-nxtgn-expired-certs.sh
/bin/make-nxtgn-cert.pl

%files pki
%defattr(-,root,root)
/etc/pki/tls/certs/ca-bundle-nxtgn-openssl.crt

%changelog
* Fri Aug 14 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20200811-1
- Initial build.  First version
