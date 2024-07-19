%define _bind_user      named
%define _bind_group     named
%define _home_dir       %{_sharedstatedir}/bind

Summary:        Domain Name System software
Name:           bindutils
Version:        9.18.27
Release:        1%{?dist}
License:        ISC
URL:            http://www.isc.org/downloads/bind/
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://downloads.isc.org/isc/bind9/%{version}/bind-%{version}.tar.xz
%define sha512  bind=d0c89821fef38e531d65b465adeb5946589775e6a4d5e2068e969f1106c961d3b202af19247b9e20f9fbde645be10d610478edf89ed0d83b39d38fb4353c693a

Patch0: bind-CVE-2024-0760.patch
Patch1: bind-CVE-2024-1737.patch
Patch2: bind-CVE-2024-1975.patch
Patch3: bind-CVE-2024-4076.patch

BuildRequires:  openssl-devel
BuildRequires:  libuv-devel
BuildRequires:  krb5-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  systemd-devel
BuildRequires:  nghttp2-devel

Requires: krb5
Requires: e2fsprogs-libs
Requires: openssl
Requires: libuv
Requires: openssl
Requires: nghttp2
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

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

%make_build

%install
%make_install -C lib %{?_smp_mflags}
%{__rm} -rf %{buildroot}%{_includedir}
%make_install -C bin/dig %{?_smp_mflags}
%make_install -C bin/nsupdate %{?_smp_mflags}

mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_tmpfilesdir} %{buildroot}%{_home_dir}
cat << EOF >> %{buildroot}/%{_sysconfdir}/named.conf
zone "." in {
    type master;
    allow-update {none;}; // no DDNS by default
};
EOF
echo "d /run/named 0755 named named - -" > %{buildroot}%{_tmpfilesdir}/named.conf

%pre
if [ $1 -eq 1 ] ; then
    if ! getent group %{_bind_group} >/dev/null; then
        groupadd -r %{_bind_group}
    fi
    if ! getent passwd %{_bind_user} >/dev/null; then
        useradd -g %{_bind_group} -d %{_home_dir}\
            -s /bin/false -M -r %{_bind_user}
    fi
fi

%post
chown -R root:%{_bind_user} %{_home_dir}
chmod 0770 %{_home_dir}
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_sysconfdir}/*
%{_home_dir}
%{_tmpfilesdir}/named.conf

%changelog
* Mon Jul 22 2024 Dweep Advani <dweep.advani@broadcom.com> 9.18.27-1
- Update to version 9.18.27 to fix CVE-2024-0760/1737/1975/4076
* Mon Feb 12 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 9.16.48-1
- Update to latest subversion to fix CVEs
* Wed Oct 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.16.42-4
- Don't delete user & group post uninstallation
* Thu Sep 28 2023 Prashant S Chauhan <psinghchauha@vmware.com> 9.16.42-3
- Change home directory permission & owner
* Thu Sep 28 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 9.16.42-2
- Fix CVE-2023-3341
* Fri Jul 14 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 9.16.42-1
- Fix CVE-2023-2829. Upgrade to version 9.16.42
* Wed Jun 21 2023 Dweep Advani <dadvani@vmware.com> 9.16.38-4
- Fix CVE-2023-2828 and CVE-2023-2911
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 9.16.38-3
- Bump version as a part of libuv upgrade
* Fri Feb 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 9.16.38-2
- Adding e2fsprogs and krb5 as dependencies to get functionality needed for SSSD.
* Thu Feb 16 2023 Harinadh D <hdommaraju@vmware.com> 9.16.38-1
- fix CVE-2022-3736
* Wed Sep 21 2022 Dweep Advani <dadvani@vmware.com> 9.16.33-1
- Version upgraded to 9.16.33 to fix multiple CVEs
- CVE-2022-2795, CVE-2022-3080,  CVE-2022-38177 and CVE-2022-38178
* Sun Mar 20 2022 Dweep Advani <dadvani@vmware.com> 9.16.27-1
- Version upgraded to 9.16.27 to address CVE-2021-25220 and CVE-2022-0396
* Fri Nov 12 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 9.16.22-2
- Bump up release for openssl
* Mon Nov 08 2021 Sujay G <gsujay@vmware.com> 9.16.22-1
- Bump version to 9.16.22 to fix CVE-2021-25219
* Tue Jun 01 2021 Sujay G <gsujay@vmware.com> 9.16.15-1
- Bump version to 9.16.15 to fix CVE-2021-25214, CVE-2021-25215, CVE-2021-25216, CVE-2020-8625
* Thu Oct 01 2020 Sujay G <gsujay@vmware.com> 9.16.6-1
- Bump version to 9.16.6
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
