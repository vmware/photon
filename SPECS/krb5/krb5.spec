Summary:        The Kerberos newtork authentication system
Name:           krb5
Version:        1.14
Release:        7%{?dist}
License:        MIT
URL:            http://cyrusimap.web.cmu.edu/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://web.mit.edu/kerberos/www/dist/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1    krb5=02973f6605b1170bec812af9c8da4e447eeca9a9
Patch0:         krb5-1.14-skip-unnecessary-mech-calls.patch
Patch1:         krb5-1.14-never-unload-mechanisms.patch
Patch2:         krb5-1.14-CVE-2015-8631.patch
Patch3:         krb5-1.14-CVE-2016-3120.patch
#Based on https://github.com/krb5/krb5/commit/56f7b1bc95a2a3eeb420e069e7655fb181ade5cf
#changed for version 1.14
Patch4:         krb5-1.14-CVE-2017-11462.patch
Requires:       openssl
Requires:       e2fsprogs
BuildRequires:  openssl-devel
BuildRequires:  e2fsprogs-devel
%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of clear text passwords.
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%build

cd src &&
sed -e "s@python2.5/Python.h@& python2.7/Python.h@g" \
    -e "s@-lpython2.5]@&,\n  AC_CHECK_LIB(python2.7,main,[PYTHON_LIB=-lpython2.7])@g" \
    -i configure.in &&
sed -e 's@\^u}@^u cols 300}@' \
    -i tests/dejagnu/config/default.exp &&
CPPFLAGS="-D_GNU_SOURCE" \
autoconf &&
./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --libdir=%{_libdir} \
        --sysconfdir=/etc \
        --localstatedir=/var/lib \
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
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/krb5/plugins/*
%{_sbindir}/*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datarootdir}/examples/*
%{_datarootdir}/locale/*
%{_datarootdir}/man/man5/.k5identity.5.gz
%{_datarootdir}/man/man5/.k5login.5.gz
%{_docdir}/%{name}-%{version}
%changelog
*   Thu Sep 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.14-7
-   Patch for CVE-2017-11462
*   Mon Jun 19 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14-6
-   Patch for CVE-2016-3120
*   Wed Apr 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.14-5
-   Patch for CVE-2015-8631
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.14-4
-   GA - Bump release of all rpms
*   Mon Mar 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  1.14-3
-   Add patch to never unload gssapi mechanisms
*   Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com>  1.14-2
-   Add patch for skipping unnecessary mech calls in gss_inquire_cred
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.14-1
-   Upgrade version
*   Tue Oct 07 2014 Divya Thaluru <dthaluru@vmware.com> 1.12.2-1
-   Initial build.  First version
