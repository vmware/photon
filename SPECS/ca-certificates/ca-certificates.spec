Summary:        Certificate Authority certificates
Name:           ca-certificates
Version:        20230315
Release:        2%{?dist}
License:        Custom
URL:            http://anduin.linuxfromscratch.org/BLFS/other
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: certdata.txt

Requires: openssl-libs
Requires: ca-certificates-pki = %{version}-%{release}
Requires(posttrans): /usr/bin/ln

BuildRequires: openssl

Provides: ca-certificates-mozilla = %{version}-%{release}

%description
The Public Key Inrastructure is used for many security issues in a
Linux system. In order for a certificate to be trusted, it must be
signed by a trusted agent called a Certificate Authority (CA). The
certificates loaded by this section are from the list on the Mozilla
version control system and formats it into a form used by
OpenSSL-1.0.1e. The certificates can also be used by other applications
either directly of indirectly through openssl.

%package             pki
Summary:             Certificate Authority certificates (pki tls certs)
Group:               System Environment/Security

%description         pki
Certificate Authority certificates (pki tls certs)

%prep -p exit

%build
install -vdm 755 %{_builddir}%{_bindir}
cp %{SOURCE0} %{_builddir}

# make-cert.pl
cat > %{_builddir}%{_bindir}/make-cert.pl << "EOF"
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
EOF
#
# make-ca.sh
#
cat > %{_builddir}%{_bindir}/make-ca.sh << "EOF"
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
CONVERTSCRIPT="%{_builddir}%{_bindir}/make-cert.pl"
SSLDIR="%{_sysconfdir}/ssl"
mkdir "${TEMPDIR}/certs"
# Get a list of staring lines for each cert
CERTBEGINLIST=$(grep -n "^# Certificate" "${certdata}" | cut -d":" -f1)
# Get a list of ending lines for each cert
CERTENDLIST=$(grep -n "^CKA_TRUST_STEP_UP_APPROVED" "${certdata}" | cut -d ":" -f 1)
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
# Remove denylisted files
# MD5 Collision Proof of Concept CA
if test -f certs/8f111d69.pem; then
  echo "Certificate 8f111d69 is not trusted!  Removing..."
  rm -f certs/8f111d69.pem
fi
# Finally, generate the bundle and clean up.
cat certs/*.pem > ${BUNDLE}
rm -r "${TEMPDIR}"
EOF
#
# remove-expired-certs.sh\
#
cat > %{_builddir}%{_bindir}/remove-expired-certs.sh << "EOF"
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
OPENSSL=%{_bindir}/openssl
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

chmod +x %{_builddir}%{_bindir}/*

printf "making certs\n"
%{_builddir}%{_bindir}/make-ca.sh
printf "Removing expired certs\n"
%{_builddir}%{_bindir}/remove-expired-certs.sh
printf "Build portion completed\n"

sed -i 's|CONVERTSCRIPT="%{_builddir}%{_bindir}/make-cert.pl"|CONVERTSCRIPT="%{_bindir}/make-cert.pl"|' %{_builddir}%{_bindir}/make-ca.sh
sed -i 's|DIR=certs|DIR=%{_sysconfdir}/ssl/certs|' %{_builddir}%{_bindir}/remove-expired-certs.sh

%install
SSLDIR=%{_sysconfdir}/ssl
install -d %{buildroot}${SSLDIR}/certs
install -d %{buildroot}%{_sysconfdir}/pki/tls/certs
cp -v certs/*.pem %{buildroot}${SSLDIR}/certs
install BLFS-ca-bundle*.crt %{buildroot}%{_sysconfdir}/pki/tls/certs/ca-bundle.crt
#ln -sfv ../$(readlink %{buildroot}/${SSLDIR}/ca-bundle.crt) %{buildroot}/${SSLDIR}/certs/ca-certificates.crt
unset SSLDIR

install -Dm644 %{_builddir}%{_bindir}/make-ca.sh %{buildroot}%{_bindir}/make-ca.sh
install -Dm644 %{_builddir}%{_bindir}/make-cert.pl %{buildroot}%{_bindir}/make-cert.pl
install -Dm644 %{_builddir}%{_bindir}/remove-expired-certs.sh %{buildroot}%{_bindir}/remove-expired-certs.sh
%{_fixperms} %{buildroot}/*

%posttrans
cd %{_sysconfdir}/ssl/certs
for file in *.pem; do
  ln -sf $file $(openssl x509 -hash -noout -in $file).0
done
exit 0

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/ssl/certs/*
%{_bindir}/make-ca.sh
%{_bindir}/remove-expired-certs.sh
%{_bindir}/make-cert.pl

%files pki
%defattr(-,root,root)
%{_sysconfdir}/pki/tls/certs/ca-bundle.crt

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 20230315-2
- Bump version as a part of openssl upgrade
* Thu Mar 16 2023 Gerrit Photon <photon-checkins@vmware.com> 20230315-1
- Automatic Version Bump
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 20220706-2
- Require openssl-libs
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 20220706-1
- Automatic Version Bump
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 20210429-2
- Fix binary path
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 20210429-1
- Automatic Version Bump
* Fri Apr 23 2021 Gerrit Photon <photon-checkins@vmware.com> 20210422-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 20210419-1
- Automatic Version Bump
* Fri Oct 02 2020 Gerrit Photon <photon-checkins@vmware.com> 20201001-1
- Automatic Version Bump
* Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 20200924-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20200922-2
- openssl 1.1.1
* Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20200922-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 20200903-1
- Automatic Version Bump
* Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 20200825-1
- Automatic Version Bump
* Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 20200709-1
- Automatic Version Bump
- Fix for OpenSSL CA certs not generated in latest tags move %post to %posttrans
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 20200708-1
- Automatic Version Bump
* Wed May 22 2019 Gerrit Photon <photon-checkins@vmware.com> 20190521-1
- Automatic Version Bump
* Tue Sep 25 2018 Ankit Jain <ankitja@vmware.com> 20180919-1
- Updating mozilla certdata.txt to latest revision
* Wed May  3 2017 Bo Gan <ganb@vmware.com> 20170406-3
- Fixed dependency on coreutils
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 20170406-2
- Added -pki subpackage
* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com> 20170406-1
- Updating mozilla certdata.txt to latest revision
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 20160109-5
- GA - Bump release of all rpms
* Wed Feb 10 2016 Anish Swaminathan <anishs@vmware.com> 20160109-4
- Add Provides field
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 20160109-3
- Force create links for certificates
* Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 20160109-2
- Remove c_rehash dependency
* Wed Jan 13 2016 Divya Thaluru <dthaluru@vmware.com> 20160109-1
- Updating mozilla certdata.txt to latest revision
* Wed Oct 15 2014 Divya Thaluru <dthaluru@vmware.com> 20130524-1
- Initial build.  First version
