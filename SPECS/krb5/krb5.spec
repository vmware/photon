Summary:        The Kerberos newtork authentication system
Name:           krb5
Version:        1.20.1
Release:        3%{?dist}
License:        MIT
URL:            http://web.mit.edu/kerberos
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://web.mit.edu/kerberos/www/dist/%{name}/1.17/%{name}-%{version}.tar.gz
%define sha512 %{name}=6f57479f13f107cd84f30de5c758eb6b9fc59171329c13e5da6073b806755f8d163eb7bd84767ea861ad6458ea0c9eeb00ee044d3bcad01ef136e9888564b6a2

Requires:       openssl-libs
Requires:       e2fsprogs-libs

BuildRequires:  bison
BuildRequires:  openssl-devel
BuildRequires:  e2fsprogs-devel

Provides:       pkgconfig(mit-krb5)
Provides:       pkgconfig(mit-krb5-gssapi)

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of clear text passwords.

%package devel
Summary:        Libraries and header files for krb5
Requires:   %{name} = %{version}-%{release}
%description devel
Static libraries and header files for the support library for krb5

%package lang
Summary:    Additional language files for krb5
Group:      System Environment/Security
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of krb5.

%prep
%autosetup -p1

%build
cd src &&
sed -e 's@\^u}@^u cols 300}@' \
    -i tests/dejagnu/config/default.exp &&
CPPFLAGS="-D_GNU_SOURCE" \
autoconf
if [ %{_host} != %{_build} ]; then
  export krb5_cv_attr_constructor_destructor=yes,yes
  export ac_cv_func_regcomp=yes
  export ac_cv_printf_positional=yes
  export ac_cv_file__etc_environment=no
  export ac_cv_file__etc_TIMEZONE=no
fi
%configure \
        --with-system-et         \
        --with-system-ss         \
        --with-system-verto=no   \
        --enable-dns-for-realm   \
        --enable-pkinit          \
        --enable-shared          \
        --without-tcl
make %{?_smp_mflags}

%install
cd src
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot}/%{_libdir} -name '*.la' -delete
for LIBRARY in gssapi_krb5 gssrpc k5crypto kadm5clnt kadm5srv \
               kdb5 krad krb5 krb5support verto ; do
    chmod -v 755 %{buildroot}/%{_libdir}/lib$LIBRARY.so
done

ln -v -sf %{buildroot}/%{_libdir}/libkrb5.so.3.3        /usr/lib/libkrb5.so
ln -v -sf %{buildroot}/%{_libdir}/libk5crypto.so.3.1    /usr/lib/libk5crypto.so
ln -v -sf %{buildroot}/%{_libdir}/libkrb5support.so.0.1 /usr/lib/libkrb5support.so

mv -v %{buildroot}/%{_bindir}/ksu /bin
chmod -v 755 /bin/ksu

install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}

unset LIBRARY
%{_fixperms} %{buildroot}/*

%check
# krb5 tests require hostname resolve
echo "127.0.0.1 $HOSTNAME" >> /etc/hosts
cd src
make check %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/krb5/plugins/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/man7/*
%{_datarootdir}/man/man5/.k5identity.5.gz
%{_datarootdir}/man/man5/.k5login.5.gz

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datarootdir}/examples/*
%{_docdir}/*

%files lang
%defattr(-,root,root)
%{_datarootdir}/locale/*

%changelog
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.20.1-3
- Require openssl-libs
* Mon Feb 20 2023 Tapas Kundu <tkundu@vmware.com> 1.20.1-2
- Add Bison in buildrequires
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.20.1-1
- Upgrade to version 1.20.1
* Fri Sep 17 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.17.2-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.17.2-1
- Downgrade to 1.17 since PMD RPC call getting failed.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.18.3-1
- Automatic Version Bump
* Mon Nov 02 2020 Tapas Kundu <tkundu@vmware.com> 1.17-4
- Fix krb5 build.
* Thu Oct 29 2020 Shreyas B. <shreyasb@vmware.com> 1.17-3
- krb5 v1.18.2 is not stable, creating panic for PMD-Client, so downgrading to v1.17.
* Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.18.2-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.17-3
- openssl 1.1.1
* Fri Nov 01 2019 Alexey Makhalov <amakhalov@vmware.com> 1.17-2
- Cross compilation support
* Thu Oct 03 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.17-1
- Update to version 1.17
* Fri Sep 14 2018 Ankit Jain <ankitja@vmware.com> 1.16.1-1
- Update to version 1.16.1
* Wed Dec 13 2017 Xiaolin Li <xiaolinl@vmware.com> 1.16-1
- Update to version 1.16 to address CVE-2017-15088
* Thu Sep 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.2-1
- Update to version 1.15.2
* Mon Jul 10 2017 Alexey Makhalov <amakhalov@vmware.com> 1.15.1-2
- Fix make check: add /etc/hosts entry, deactivate parallel check
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.15.1-1
- Updated to version 1.51.1
* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 1.14-6
- Added -lang and -devel subpackages
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 1.14-5
- Use e2fsprogs-libs as runtime deps
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.14-4
- GA - Bump release of all rpms
* Mon Mar 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  1.14-3
- Add patch to never unload gssapi mechanisms
* Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com>  1.14-2
- Add patch for skipping unnecessary mech calls in gss_inquire_cred
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.14-1
- Upgrade version
* Tue Oct 07 2014 Divya Thaluru <dthaluru@vmware.com> 1.12.2-1
- Initial build. First version
