%global _default_patch_fuzz 2
%global debug_package %{nil}

Summary:        OpenLdap-2.4.43
Name:           openldap
Version:        2.4.53
Release:        2%{?dist}
License:        OpenLDAP
URL:            http://cyrusimap.web.cmu.edu/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{name}-%{version}.tgz
%define sha1 openldap=9a03db5cc02fd8b0afc5bf11fb10f7cd5260bcf0

Patch0:         openldap-2.4.51-consolidated-2.patch

Requires:       openssl >= 1.0.1, cyrus-sasl >= 2.1

BuildRequires:  cyrus-sasl >= 2.1
BuildRequires:  openssl-devel >= 1.0.1
BuildRequires:	groff
BuildRequires:	e2fsprogs-devel
BuildRequires:  libtool
BuildRequires:  systemd

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%prep
%setup -q
%patch0 -p1

%build
autoconf

sed -i '/6.0.20/ a\\t__db_version_compat' configure

export CPPFLAGS="-D_REENTRANT -DLDAP_CONNECTIONLESS -D_GNU_SOURCE -D_AVL_H"

%configure \
         $(test %{_host} != %{_build} && echo "CC=%{_host}-gcc --with-yielding-select=yes --with-sysroot=/target-%{_arch}") \
        --disable-static     \
        --disable-slapd      \
        --with-tls=openssl   \
        --enable-debug       \
        --prefix=/usr        \
        --enable-dynamic     \
        --enable-syslog      \
        --enable-ipv6        \
        --enable-local       \
        --enable-crypt       \
        --enable-spasswd     \
        --enable-modules     \
        --enable-backends    \
        --disable-ndb --enable-overlays=mod \
        --with-cyrus-sasl    \
        --with-threads

  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool


if [ %{_host} != %{_build} ]; then
 sed -i '/#define NEED_MEMCMP_REPLACEMENT 1/d' include/portable.h
fi
make depend
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*

chmod a+x %{buildroot}%{_libdir}/liblber.so*
chmod a+x %{buildroot}%{_libdir}/libldap_r.so*

pushd %{buildroot}%{_libdir}
v=%{version}
version=$(echo ${v%.[0-9]*})
for lib in liblber libldap libldap_r libslapi; do
  rm -f ${lib}.so
  ln -s ${lib}-${version}.so.2 ${lib}.so
done
popd

%check
make %{?_smp_mflags} test

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%dir %{_sysconfdir}/openldap
%{_sysconfdir}/openldap/*
%{_libdir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.53-2
-   openssl 1.1.1
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.53-1
-   Automatic Version Bump
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.52-1
-   Automatic Version Bump
*   Wed Aug 26 2020 Piyush Gupta <gpiyush@vmware.com> 2.4.51-2
-   Release bump up
*   Fri Aug 14 2020 Susant Sahani <ssahani@vmware.com> 2.4.51-1
-   Version Bump and fix build
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.50-1
-   Automatic Version Bump
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 2.4.46-3
-   Cross compilation support
*   Mon Nov 5 2018 Sriram Nambakam <snambakam@vmware.com> 2.4.46-2
-   export CPPFLAGS before invoking configure
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.4.46-1
-   Upgrade to 2.4.46
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.44-3
-   Use standard configure macros
*   Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.44-2
-   Applied patch for CVE-2017-9287
*   Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.44-1
-   Update to 2.4.44
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.4.43-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.43-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.43-1
-   Updated to version 2.4.43
*   Fri Aug 14 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.40-2
-   Patches for CVE-2015-1545 and CVE-2015-1546.
*   Wed Oct 08 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.40-1
-   Initial build.	First version
