Summary:        Domain Name System software
Name:           bindutils
Version:        9.16.15
Release:        1%{?dist}
License:        ISC
URL:            http://www.isc.org/downloads/bind/
Source0:        ftp://ftp.isc.org/isc/bind9/%{version}/bind-%{version}.tar.xz
%define sha1    bind=5d68bbd1ff452708d45f2d4ef832faa3a1690fc7
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       openssl
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
BuildRequires:  openssl-devel
BuildRequires:  libuv-devel

%description
BIND is open source software that implements the Domain Name System (DNS) protocols
for the Internet. It is a reference implementation of those protocols, but it is
also production-grade software, suitable for use in high-volume and high-reliability applications.

%prep
%setup -qn bind-%{version}

%build
%configure \
    --without-python \
    --disable-linux-caps
make -C lib/dns %{?_smp_mflags}
make -C lib/isc %{?_smp_mflags}
make -C lib/bind9 %{?_smp_mflags}
make -C lib/isccfg %{?_smp_mflags}
make -C lib/irs %{?_smp_mflags}
make -C bin/dig %{?_smp_mflags}

%install
make -C bin/dig DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
mkdir -p %{buildroot}/%{_sysconfdir}
mkdir -p %{buildroot}/%{_prefix}/lib/tmpfiles.d
cat << EOF >> %{buildroot}/%{_sysconfdir}/named.conf
zone "." in {
    type master;
    allow-update {none;}; // no DDNS by default
};
EOF
echo "d /run/named 0755 named named - -" > %{buildroot}/%{_prefix}/lib/tmpfiles.d/named.conf

%pre
if ! getent group named >/dev/null; then
    groupadd -r named
fi
if ! getent passwd named >/dev/null; then
    useradd -g named -d /var/lib/bind\
        -s /bin/false -M -r named
fi
%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if getent passwd named >/dev/null; then
    userdel named
fi
if getent group named >/dev/null; then
    groupdel named
fi

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sysconfdir}/*
%{_prefix}/lib/tmpfiles.d/named.conf

%changelog
*   Wed May 12 2021 Sujay G <gsujay@vmware.com> 9.16.15-1
-   Bump version to 9.16.15 to fix CVE-2021-25214, CVE-2021-25215, CVE-2021-25216
*   Fri Mar 05 2021 Dweep Advani <dadvani@vmware.com> 9.16.6-2
-   Patched for CVE-2020-8625
*   Fri Aug 28 2020 Sujay G <gsujay@vmware.com> 9.16.6-1
-   Bump version to 9.16.6
*   Fri Jul 10 2020 Sujay G <gsujay@vmware.com> 9.16.4-1
-   Bump version to 9.16.4 to fix CVE-2020-8618 & CVE-2020-8619
*   Thu May 28 2020 Sujay G <gsujay@vmware.com> 9.16.3-1
-   Bump veresion to 9.16.3 to fix CVE-2020-8616 & CVE-2020-8617
*   Mon Feb 17 2020 Sujay G <gsujay@vmware.com> 9.15.6-1
-   Bump version to 9.15.6 to fix CVE-2019-6470
*   Mon Jan 27 2020 Tapas Kundu <tkundu@vmware.com> 9.15.5-2
-   Bump bindutils release to build with latest openssl
*   Thu Jan 09 2020 Sujay G <gsujay@vmware.com> 9.15.5-1
-   Bump bindutils version to 9.15.5
*   Sun Sep 23 2018 Sujay G <gsujay@vmware.com> 9.13.3-1
-   Bump bindutils version to 9.13.3
*   Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 9.10.6-1
-   Upgrading version to 9.10.6-P1, fix CVE-2017-3145
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 9.10.4-4
-   Remove shadow from requires and use explicit tools for post actions
*   Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 9.10.4-3
-   Upgrading version to 9.10.4-P8
*   Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.4-2
-   add shadow to requires
*   Mon Jun 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 9.10.4-1
-   Upgraded the version to 9.10.4
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.3-3
-   GA - Bump release of all rpms
*   Fri Apr 29 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-2
-   Add group named and user named
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-1
-   Updated to version 9.10.3
*   Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-1
-   Fixing release
*   Tue Jan 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-P1
-   Initial build. First version
