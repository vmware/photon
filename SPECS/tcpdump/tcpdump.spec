Summary:	Packet Analyzer
Name:		tcpdump
Version:	4.7.3	
Release:	1%{?dist}
License:	BSD
URL:		http://www.tcpdump.org
Source0:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
%define sha1 tcpdump=4f085cef7cd4aedc9e402021ec11e3a8b23a6926
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
*   Mon Apr 6  2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.7.3-1
-   Updating version to 4.7.3
