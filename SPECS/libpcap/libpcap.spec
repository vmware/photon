Summary:	C/C++ library for network traffic capture
Name:		libpcap
Version:	1.8.1
Release:	1%{?dist}
License:	BSD
URL:		http://www.tcpdump.org
Source0:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
%define sha1 libpcap=32d7526dde8f8a2f75baf40c01670602aeef7e39
Group:		Networking/Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
%description
libpcap provides functions for user-level packet capture, used in low-level network monitoring.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*.h
%{_includedir}/pcap/*.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%changelog
*	Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.1-1
-	Updated to version 1.8.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.4-2
-	GA - Bump release of all rpms
* 	Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
- 	Updated to version 1.7.4
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.7.2-1
-   Version upgrade to 1.7.2
*	Wed Jan 21 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.2-1
-	Initial build. First version
