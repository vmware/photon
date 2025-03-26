Summary:        The Kerberos newtork authentication system
Name:           krb5
Version:        1.17
Release:        13%{?dist}
License:        MIT
URL:            http://web.mit.edu/kerberos
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://web.mit.edu/kerberos/www/dist/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=7462a578b936bd17f155a362dbb5d388e157a80a096549028be6c55400b11361c7f8a28e424fd5674801873651df4e694d536cae66728b7ae5e840e532358c52

Patch0: krb5-CVE-2020-28196.patch
Patch1: krb5-CVE-2021-36222.patch
Patch2: krb5-CVE-2021-37750.patch
%if 0%{?with_check}
Patch3: krb5-Make-test-PKINIT-certs-work-with-OpenSSL-3.0.patch
%endif
Patch4: krb5-CVE-2022-42898.patch
Patch5: CVE-2023-36054.patch
Patch6: CVE-2024-26458.patch
Patch7: CVE-2024-26461.patch
Patch8: CVE-2024-37370-37371.patch

Requires:       openssl
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
Summary:    Libraries and header files for krb5
Requires:   %{name} = %{version}-%{release}
Requires:  e2fsprogs-devel
%description devel
Static libraries and header files for the support library for krb5

%package lang
Summary:    Additional language files for krb5
Group:      System Environment/Security
Requires:   %{name} = %{version}-%{release}
%description lang
These are the additional language files of krb5.

%prep
%autosetup -p1

%build
cd src && \
sed -e 's@\^u}@^u cols 300}@' \
    -i tests/dejagnu/config/default.exp && \
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
find %{buildroot}%{_libdir} -name '*.la' -delete
for LIBRARY in gssapi_krb5 gssrpc k5crypto kadm5clnt kadm5srv \
               kdb5 krad krb5 krb5support verto ; do
    chmod -v 755 %{buildroot}/%{_libdir}/lib$LIBRARY.so
done

ln -sfv %{buildroot}%{_libdir}/libkrb5.so.3.3        %{_libdir}/libkrb5.so
ln -sfv %{buildroot}%{_libdir}/libk5crypto.so.3.1    %{_libdir}/libk5crypto.so
ln -sfv %{buildroot}%{_libdir}/libkrb5support.so.0.1 %{_libdir}/libkrb5support.so

mv -v %{buildroot}/%{_bindir}/ksu /bin
chmod -v 755 /bin/ksu

install -v -dm755 %{buildroot}%{_docdir}/%{name}-%{version}

unset LIBRARY
%{_fixperms} %{buildroot}/*

%check
# krb5 tests require hostname resolve
echo "127.0.0.1 $HOSTNAME" >> /etc/hosts
cd src
pushd tests/dejagnu/pkinit-certs
sh make-certs.sh
popd
# make doesn't support _smp_mflags
make check

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
* Fri Aug 30 2024 Harinadh D <harinadh.dommaraju@broadcom.com> 1.17-13
- Include e2fsprogs-devel as Requires for krb5 devel package
- This needed to resolve linking issues in elfutils build
* Fri Aug 30 2024 Harinadh D <harinadh.dommaraju@broadcom.com> 1.17-12
- patched CVE-2024-37370,CVE-2024-37371
* Mon Jun 03 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 1.17-11
- patched CVE-2024-26458 and CVE-2024-26461
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 1.17-10
- Fix CVE-2023-36054
* Thu Jan 19 2023 Srish Srinivasan <ssrish@vmware.com> 1.17-9
- Fix for CVE-2022-42898
* Mon Jan 09 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.17-8
- Update due to change in e2fsprogs version
* Tue Nov 30 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.17-7
- Fix for CVE-2020-28196/CVE-2021-36222/CVE-2021-37750
* Fri Sep 17 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.17-6
- Bump up release for openssl
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 1.17-5
- Replacement of ITS suggested words.
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
