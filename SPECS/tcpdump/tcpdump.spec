Summary:	Packet Analyzer
Name:		tcpdump
Version:	4.7.4	
Release:	2%{?dist}
License:	BSD
URL:		http://www.tcpdump.org
Source0:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
%define sha1 tcpdump=a18c9dbc4b5c4983af9cb52d8e473f5504546f4a
Group:		Networking
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires: 	libpcap
Requires:	libpcap
%description
Tcpdump is a common packet analyzer that runs under the command line. 
It allows the user to display TCP/IP and other packets being 
transmitted or received over a network to which the computer is attached.
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
%{_sbindir}/*
%{_mandir}/man1/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	4.7.4	-2
-	GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.7.4-1
-   Upgrade version.
*   Mon Apr 6  2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.7.3-1
-   Updating version to 4.7.3
