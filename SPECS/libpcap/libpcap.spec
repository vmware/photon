Summary:	C/C++ library for network traffic capture
Name:		libpcap
Version:	1.7.2	
Release:	1%{?dist}
License:	BSD
URL:		http://www.tcpdump.org
Source0:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
%define sha1 libpcap=97aed0270bc201dfdeacccddc61179d27c68e42c
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

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.7.2-1
-   Version upgrade to 1.7.2
*	Wed Jan 21 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.2-1
-	Initial build. First version
