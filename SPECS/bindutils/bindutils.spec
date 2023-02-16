Summary:        Domain Name System software
Name:           bindutils
Version:        9.16.38
Release:        1%{?dist}
License:        ISC
URL:            http://www.isc.org/downloads/bind/
Source0:        https://downloads.isc.org/isc/bind9/%{version}/bind-%{version}.tar.xz
%define sha512  bind=fe95681b95ce90aee019e1bdcedba104f7bd968915853321205176c29eedd8df6e04682380adaa332aec06c1cc6537f431d5e21d09f756f45c2d780e8bc80435
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
%autosetup -p1 -n bind-%{version}

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
make -C bin/dig DESTDIR=%{buildroot} install %{?_smp_mflags}
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

%posttrans
if [ $1 -eq 1 ] ; then
    if ! getent group named >/dev/null; then
        groupadd -r named
    fi
    if ! getent passwd named >/dev/null; then
        useradd -g named -d /var/lib/bind\
            -s /bin/false -M -r named
    fi
fi

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
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
%{_sysconfdir}/*
%{_prefix}/lib/tmpfiles.d/named.conf

%changelog
*   Thu Feb 16 2023 Harinadh D <hdommaraju@vmware.com> 9.16.38-1
-   fix CVE-2022-3736
*   Wed Sep 21 2022 Dweep Advani <dadvani@vmware.com> 9.16.33-1
-   Version upgraded to 9.16.33 to fix multiple CVEs
-   CVE-2022-2795, CVE-2022-3080,  CVE-2022-38177 and CVE-2022-38178
*   Sun Mar 20 2022 Dweep Advani <dadvani@vmware.com> 9.16.27-1
-   Version upgraded to 9.16.27 to address CVE-2021-25220 and CVE-2022-0396
*   Fri Nov 12 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 9.16.22-2
-   Bump up release for openssl
*   Mon Nov 08 2021 Sujay G <gsujay@vmware.com> 9.16.22-1
-   Bump version to 9.16.22 to fix CVE-2021-25219
*   Tue Jun 01 2021 Sujay G <gsujay@vmware.com> 9.16.15-1
-   Bump version to 9.16.15 to fix CVE-2021-25214, CVE-2021-25215, CVE-2021-25216, CVE-2020-8625
*   Thu Oct 01 2020 Sujay G <gsujay@vmware.com> 9.16.6-1
-   Bump version to 9.16.6
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 9.16.4-2
-   openssl 1.1.1
*   Fri Jul 10 2020 Sujay G <gsujay@vmware.com> 9.16.4-1
-   Bump version to 9.16.4 to fix CVE-2020-8618 & CVE-2020-8619
*   Tue Jun 02 2020 Sujay G <gsujay@vmware.com> 9.16.3-1
-   Bump version to 9.16.3
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
