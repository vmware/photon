%global __requires_exclude perl\\(.*\\)
Summary:	Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6. 
Name:		net-snmp   
Version:	5.7.3
Release:	5%{?dist}
License:	BSD (like)  
URL:		http://net-snmp.sourceforge.net/
Group:		Productivity/Networking/Other
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1 net-snmp=97dc25077257680815de44e34128d365c76bd839
Patch1: 	net-snmp-5.7.2-systemd.patch
BuildRequires:	openssl-devel perl systemd
Requires:	perl systemd
%description
 Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6.

%package devel
Group: Development/Libraries
Summary: The includes and static libraries from the Net-SNMP package.
Requires: net-snmp = %{version}

%description devel
The net-snmp-devel package contains headers and libraries for building SNMP applications.

%prep
%setup -q
%patch1 -p1

%build
./configure --prefix=%{_prefix} \
		--host=ia64-linux \
		--build=i686 \
		--target=ia64-linux \
		--sbindir=/sbin \
		--with-sys-location="unknown" \
		--with-logfile=/var/log/net-snmpd.log \
		--with-persistent-directory=/var/lib/net-snmp \
		--with-sys-contact="root@localhost" \
		--with-defaults \
		--with-systemd \
		--disable-static \
		--with-x=no \
		--enable-as-needed
make

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/snmpd.service
[Unit]
Description=Simple Network Management Protocol (SNMP) Daemon.
After=syslog.target network.target

[Service]
Type=notify
ExecStart=/usr/sbin/snmpd -LS0-6d -f
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
EOF

cat << EOF >> %{buildroot}/lib/systemd/system/snmptrapd.service
[Unit]
Description=Simple Network Management Protocol (SNMP) Trap Daemon.
After=syslog.target network.target

[Service]
Type=notify
ExecStart=/usr/sbin/snmptrapd -Lsd -f
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
EOF

%check
make %{?_smp_mflags} test

%post
/sbin/ldconfig
%systemd_post snmpd.service
%systemd_post snmptrapd.service

%preun
%systemd_preun snmpd.service
%systemd_preun snmptrapd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart snmpd.service
%systemd_postun_with_restart snmptrapd.service

%clean
rm -rf %{buildroot}/*
 
%files
%doc COPYING NEWS README ChangeLog
%defattr(-,root,root)
/lib/systemd/system/snmpd.service
/lib/systemd/system/snmptrapd.service
%{_bindir}
%{_libdir}/*.so.*
/sbin/*  

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}/*.la
%{_libdir}/perl5
%{_libdir}/*.so
%{_datadir}
%exclude /usr/lib/perl5/5.22.1/x86_64-linux-thread-multi/perllocal.pod

%changelog
*       Mon Oct 04 2016 ChangLee <changLee@vmware.com> 5.7.3-5
-       Modified %check
*       Thu May 26 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.7.3-4
-	Excluded the perllocal.pod log.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.7.3-3
-	GA - Bump release of all rpms
*	Wed May 04 2016 Nick Shi <nshi@vmware.com> 5.7.3-2
-	Add snmpd and snmptrapd to systemd service.
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.7.3-1
-	Initial build.	First version
