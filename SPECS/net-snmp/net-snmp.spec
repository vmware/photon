Summary:	Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6. 
Name:		net-snmp   
Version:	5.7.3
Release:	1%{?dist}
License:	BSD (like)  
URL:		http://net-snmp.sourceforge.net/
Group:		Productivity/Networking/Other
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1 net-snmp=97dc25077257680815de44e34128d365c76bd839
BuildRequires: openssl-devel 
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
		--disable-static \
		--enable-as-needed
make

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}/*
 
%files
%doc COPYING NEWS README ChangeLog
%defattr(-,root,root)
%{_bindir}
%{_libdir}/*.so.*
/sbin/

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}/*.la
%{_libdir}/perl5
%{_libdir}/*.so
%{_datadir}

%changelog
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.7.3-1
-	Initial build.	First version
