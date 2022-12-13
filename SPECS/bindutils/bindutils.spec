Summary:        Domain Name System software
Name:           bindutils
Version:        9.19.7
Release:        1%{?dist}
License:        ISC
URL:            http://www.isc.org/downloads/bind
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.isc.org/isc/bind9/%{version}/bind-%{version}.tar.xz
%define sha512    bind=c4872daf71f4c0c108a2f0a68bf0b7ee12b6490d1ae7955419847c255bc5fcd092f935fa6ea68ae53db0510e7e9af13b6ab05cb0ca0058cb13339ccbda4ede43

Requires:       openssl
Requires:       %{name}-libs = %{version}-%{release}
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

BuildRequires:  openssl-devel
BuildRequires:  libuv-devel
BuildRequires:  nghttp2-devel
BuildRequires:  libcap-devel
BuildRequires:  systemd-rpm-macros

%description
BIND is open source software that implements the Domain Name System (DNS) protocols
for the Internet. It is a reference implementation of those protocols, but it is
also production-grade software, suitable for use in high-volume and high-reliability applications.

%package    libs
Summary:    Libraries used by the BIND DNS packages
Group:      Development/Libraries

%description    libs
Contains heavyweight version of BIND suite libraries used by both named DNS
server and utilities in bindutils package.

%package    devel
Summary:    Header files and libraries needed for bind-dyndb-ldap
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description    devel
The bindutils-devel package contains full version of the header files and libraries.
Upstream no longer supports nor recommends bind libraries for third party applications.

%prep
%autosetup -p1 -n bind-%{version}

%build
%configure \
    --without-python \
    --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_tmpfilesdir}

cat << EOF >> %{buildroot}/%{_sysconfdir}/named.conf
zone "." in {
    type master;
    allow-update {none;}; // no DDNS by default
};
EOF
echo "d /run/named 0755 named named - -" > %{buildroot}%{_tmpfilesdir}/named.conf

%posttrans
if [ $1 -eq 1 ]; then
  if ! getent group named >/dev/null; then
   groupadd -r named
  fi
  if ! getent passwd named >/dev/null; then
    useradd -g named -d /var/lib/bind -s /bin/false -M -r named
  fi
fi

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  if getent passwd named >/dev/null; then
    userdel named
  fi
  if getent group named >/dev/null; then
    groupdel named
  fi
fi

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_sysconfdir}/*
%{_tmpfilesdir}/named.conf
%{_mandir}/man1/*

%files libs
%defattr(-,root,root)
%{_libdir}/libbind9.so
%{_libdir}/libdns.so
%{_libdir}/libirs.so
%{_libdir}/libisc.so
%{_libdir}/libisccc.so
%{_libdir}/libisccfg.so
%{_libdir}/libns.so
%{_libdir}/libbind9-%{version}*.so
%{_libdir}/libisccc-%{version}*.so
%{_libdir}/libns-%{version}*.so
%{_libdir}/libdns-%{version}*.so
%{_libdir}/libirs-%{version}*.so
%{_libdir}/libisc-%{version}*.so
%{_libdir}/libisccfg-%{version}*.so
%{_libdir}/bind/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/ns/*.h
%{_includedir}/dns/*.h
%{_includedir}/dst/*.h
%{_includedir}/isc/*.h
%{_includedir}/irs/*.h
%{_includedir}/isccc/*.h
%{_includedir}/isccfg/*.h
%{_includedir}/bind9/*.h
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 9.19.7-1
- Automatic Version Bump
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 9.19.4-1
- Automatic Version Bump
* Wed Mar 30 2022 Dweep Advani <dadvani@vmware.com> 9.18.1-1
- Version upgraded to 9.18.1 to address CVE-2021-25220 and CVE-2022-0396
- Add libs & devel sub packages
* Tue Mar 29 2022 Tapas Kundu <tkundu@vmware.com> 9.16.15-3
- Do not remove user and group in postun unless uninstalled
* Fri Nov 12 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 9.16.15-2
- Bump up release for openssl
* Mon Jun 07 2021 Sujay G <gsujay@vmware.com> 9.16.15-1
- Bump version to 9.16.15
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 9.16.13-1
- Automatic Version Bump
* Thu Oct 01 2020 Sujay G <gsujay@vmware.com> 9.16.6-1
- Bumper version to 9.16.6
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 9.16.4-2
- openssl 1.1.1
* Fri Jul 10 2020 Sujay G <gsujay@vmware.com> 9.16.4-1
- Bump version to 9.16.4 to fix CVE-2020-8618 & CVE-2020-8619
* Tue Jun 02 2020 Sujay G <gsujay@vmware.com> 9.16.3-1
- Bump version to 9.16.3
* Thu Jan 09 2020 Sujay G <gsujay@vmware.com> 9.15.5-1
- Bump bindutils version to 9.15.5
* Sun Sep 23 2018 Sujay G <gsujay@vmware.com> 9.13.3-1
- Bump bindutils version to 9.13.3
* Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 9.10.6-1
- Upgrading version to 9.10.6-P1, fix CVE-2017-3145
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 9.10.4-4
- Remove shadow from requires and use explicit tools for post actions
* Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 9.10.4-3
- Upgrading version to 9.10.4-P8
* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.4-2
- add shadow to requires
* Mon Jun 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 9.10.4-1
- Upgraded the version to 9.10.4
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.3-3
- GA - Bump release of all rpms
* Fri Apr 29 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-2
- Add group named and user named
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-1
- Updated to version 9.10.3
* Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-1
- Fixing release
* Tue Jan 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-P1
- Initial build. First version
