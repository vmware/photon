Summary:        ulogd - The userspace logging daemon for netfilter
Name:           ulogd
Version:        2.0.7
Release:        1%{?dist}
License:        GPLv2+
URL:            https://git.netfilter.org/ulogd2/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.netfilter.org/pub/ulogd/%{name}-%{version}.tar.bz2
%define sha1 ulogd=f2d90469e2842e2bfbe19c55cf6d56ac107aa4b9
Source1:        ulogd.service
BuildRequires:  mysql-devel libpcap-devel sqlite-devel
BuildRequires:  libnfnetlink-devel libtirpc-devel pkg-config
BuildRequires:  systemd-devel
Requires:       systemd
Patch0:         compilation-fix-for-ulogd-mysql.patch

%description
ulogd is a logging daemon that reads event messages coming from the
Netfilter connection tracking, the Netfilter packet logging subsystem
and from the Netfilter accounting subsystem.

%package mysql
Summary: MySQL output plugin for ulogd-2
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description mysql
ulogd-mysql is a MySQL output plugin for ulogd.

%package sqlite
Summary: sqlite output plugin for ulogd-2
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description sqlite
ulogd-sqlite is a sqlite output plugin for ulogd.

%package pcap
Summary: pcap output plugin for ulogd-2
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description pcap
ulogd-pcap is a pcap  output plugin for ulogd.


%prep
%setup   -q
%patch0  -p1

%build
%configure --enable-static=no \
           --enable-nfacct=no --enable-nflog=no \
           --enable-nfct=no \
	   --with-dbi-lib=%{_libdir} \
	   --with-pcap-lib=%{_libdir} \
	   --with-sqlite3-lib=%{_libdir}
make %{?_smp_mflags}

%install

rm -rf %{buildroot}
install -vd %{buildroot}/%{_sysconfdir}
install -vd %{buildroot}/%{_libdir}/ulogd
install -vd %{buildroot}/%{_sbindir}/sbin
install -vd %{buildroot}/%{_mandir}/man8
install -vd %{buildroot}/%{_libdir}/systemd/system/
install -vd %{buildroot}/var/log/ulogd/
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/lib/systemd/system/ulogd.service
install -p -m 644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/
install -p -m 644 ulogd.conf %{buildroot}%{_sysconfdir}/ulogd.conf
install ulogd.8 %{buildroot}/%{_mandir}/man8/ulogd.8
find %{buildroot} -name '*.la' -delete

%post
/sbin/ldconfig
%systemd_post ulogd.service

%preun
%systemd_preun ulogd.service

%postun
/sbin/ldconfig
%systemd_postun  ulogd.service

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root,0755)
%{_sbindir}/ulogd
%{_libdir}/ulogd
%defattr(0644,root,root,0755)
%doc COPYING
%doc AUTHORS README
%doc %{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/ulogd.conf
%{_libdir}/systemd/system/ulogd.service
%dir %{_localstatedir}/log/ulogd
%exclude %{_libdir}/ulogd/*.la
%exclude %{_libdir}/ulogd/ulogd_output_MYSQL.so
%exclude %{_libdir}/ulogd/ulogd_output_PCAP.so
%exclude %{_libdir}/ulogd/ulogd_output_SQLITE3.so

%files mysql
%defattr(0644,root,root,0755)
%{_libdir}/ulogd/ulogd_output_MYSQL.so


%files sqlite
%defattr(0644,root,root,0755)
%{_libdir}/ulogd/ulogd_output_SQLITE3.so

%files pcap
%defattr(0644,root,root,0755)
%{_libdir}/ulogd/ulogd_output_PCAP.so

%changelog
*   Tue Jul 02 2019 Vikash Bansal <bvikas@vmware.com> 2.0.7-1
-   Added ulogd package to photon-3.0