%define ssl_certs_dir %{_sysconfdir}/ssl/certs
%define crt_dir       %{_sysconfdir}/pki/tls/certs
%global __requires_exclude  perl

Summary:        Certificate Authority certificates
Name:           ca-certificates
Version:        20230315
Release:        6%{?dist}
URL:            http://anduin.linuxfromscratch.org/BLFS/other
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: certdata.txt
Source1: make-ca.sh
Source2: make-cert.pl
Source3: remove-expired-certs.sh

Source4: license.txt
%include %{SOURCE4}

Source5: make-cert.sh

Requires: openssl-libs
Requires: %{name}-pki = %{version}-%{release}
Requires(posttrans): /usr/bin/ln

BuildRequires: openssl

Provides: %{name}-mozilla = %{version}-%{release}

%description
The Public Key Inrastructure is used for many security issues in a
Linux system. In order for a certificate to be trusted, it must be
signed by a trusted agent called a Certificate Authority (CA). The
certificates loaded by this section are from the list on the Mozilla
version control system and formats it into a form used by
OpenSSL-1.0.1e. The certificates can also be used by other applications
either directly of indirectly through openssl.

%package    pki
Summary:    Certificate Authority certificates (pki tls certs)
Group:      System Environment/Security

%description pki
Certificate Authority certificates (pki tls certs)

%prep
%build
cp %{SOURCE0} %{_builddir}

echo "Making certs ..."
bash %{SOURCE1}

echo "Removing expired certs ..."
bash %{SOURCE3}

%install
install -d %{buildroot}%{ssl_certs_dir}
install -d %{buildroot}%{crt_dir}
cp -v certs/*.pem %{buildroot}%{ssl_certs_dir}
install BLFS-ca-bundle*.crt %{buildroot}%{crt_dir}/ca-bundle.crt
unset SSLDIR

mkdir -p %{buildroot}%{_bindir}
cp -pv %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE5} %{buildroot}%{_bindir}
chmod +x %{buildroot}%{_bindir}/*

pushd %{buildroot}%{ssl_certs_dir}
for file in *.pem; do
  ln -sf $file $(openssl x509 -subject_hash -noout -in $file).0
done

bash %{buildroot}%{_bindir}/remove-expired-certs.sh "${PWD}"
popd

%{_fixperms} %{buildroot}/*

%posttrans
bash %{_bindir}/remove-expired-certs.sh %{ssl_certs_dir} || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{ssl_certs_dir}/*
%{_bindir}/make-ca.sh
%{_bindir}/remove-expired-certs.sh
%{_bindir}/make-cert.pl
%{_bindir}/make-cert.sh

%files pki
%defattr(-,root,root)
%{crt_dir}/ca-bundle.crt

%changelog
* Thu Nov 21 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20230315-6
- Cleanup make-ca.sh
- Tweak remove-expired-certificates script to do the removal properly
- Add a bash script equivalent of make-cert.pl, useful in minimal deployments
* Mon Nov 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20230315-5
- Check for openssl binary presence in remove expired certs script
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20230315-4
- Release bump for SRP compliance
* Fri Mar 22 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20230315-3
- Spec cleanups, don't generate helper scripts everytime
- Create cert symlinks at build time
* Mon Jan 08 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20230315-2
- Clean up broken symlinks for which files are not present
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
