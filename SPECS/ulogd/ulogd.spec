Summary:        ulogd - The userspace logging daemon for netfilter
Name:           ulogd
Version:        2.0.7
Release:        4%{?dist}
License:        GPLv2+
URL:            https://git.netfilter.org/ulogd2
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.netfilter.org/pub/ulogd/%{name}-%{version}.tar.bz2
%define sha512 %{name}=1ad12bcf91bebe8bf8580de38693318cdabd17146f1f65acf714334885cf13adf5f783abdf2dd67474ef12f82d2cfb84dd4859439bc7af10a0df58e4c7e48b09

Source1: %{name}.service

Patch0: compilation-fix-for-ulogd-mysql.patch

BuildRequires: libpcap-devel
BuildRequires: sqlite-devel
BuildRequires: libnfnetlink-devel
BuildRequires: libtirpc-devel
BuildRequires: pkg-config
BuildRequires: mysql-devel
BuildRequires: systemd-devel

Requires: systemd
Requires: libnfnetlink

%description
ulogd is a logging daemon that reads event messages coming from the
Netfilter connection tracking, the Netfilter packet logging subsystem
and from the Netfilter accounting subsystem.

%package mysql
Summary: MySQL output plugin for ulogd-2
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: mysql

%description mysql
ulogd-mysql is a MySQL output plugin for ulogd.

%package sqlite
Summary: sqlite output plugin for ulogd-2
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: sqlite-libs

%description sqlite
ulogd-sqlite is a sqlite output plugin for ulogd.

%package pcap
Summary: pcap output plugin for ulogd-2
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: libpcap

%description pcap
ulogd-pcap is a pcap  output plugin for ulogd.

%prep
%autosetup -p1

%build
%configure \
   --enable-static=no \
   --enable-nfacct=no \
   --enable-nflog=no \
   --enable-nfct=no \
   --with-dbi-lib=%{_libdir} \
   --with-pcap-lib=%{_libdir} \
   --with-sqlite3-lib=%{_libdir}

%make_build

%install
install -vd %{buildroot}%{_sysconfdir}
install -vd %{buildroot}%{_mandir}/man8
install -vd %{buildroot}%{_unitdir}
install -vd %{buildroot}%{_var}/log/%{name}/
%make_install %{?_smp_mflags}

install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install %{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root,0755)
%{_sbindir}/%{name}
%{_libdir}/%{name}
%exclude %{_libdir}/%{name}/%{name}_output_MYSQL.so
%exclude %{_libdir}/%{name}/%{name}_output_PCAP.so
%exclude %{_libdir}/%{name}/%{name}_output_SQLITE3.so
%defattr(0644,root,root,0755)
%{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_unitdir}/%{name}.service
%dir %{_var}/log/%{name}

%files mysql
%defattr(0644,root,root,0755)
%{_libdir}/%{name}/%{name}_output_MYSQL.so

%files sqlite
%defattr(0644,root,root,0755)
%{_libdir}/%{name}/%{name}_output_SQLITE3.so

%files pcap
%defattr(0644,root,root,0755)
%{_libdir}/%{name}/%{name}_output_PCAP.so

%changelog
* Fri Nov 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.7-4
- Bump version as a part of mysql upgrade
* Thu Feb 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.7-3
- Fix the file packaging to mitigate conflicts
* Fri Jan 27 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.7-2
- Bump version as a part of mysql upgrade
* Tue Jul 02 2019 Vikash Bansal <bvikas@vmware.com> 2.0.7-1
- Added ulogd package to photon-3.0
