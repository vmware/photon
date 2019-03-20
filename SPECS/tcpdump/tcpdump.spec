Summary:	Packet Analyzer
Name:		tcpdump
Version:	4.9.2
Release:	2%{?dist}
License:	BSD
URL:		http://www.tcpdump.org
Source0:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
%define sha1 tcpdump=e2db246a9dd19278bac1a5ff875106c75e0a16d4
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
%setup -qn tcpdump-tcpdump-%{version}
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
*   Wed Mar 20 2019 Tapas Kundu <tkundu@vmware.com> 4.9.2-2
-   Bumped up to use latest openssl
*   Fri Sep 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.2-1
-   Updating version to 4.9.2
*   Thu Sep 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.1-2
-   Fix for CVE-2017-11541 CVE-2017-11542 CVE-2017-11543
*   Thu Aug 03 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.1-1
-   Updating version to 4.9.1
*       Thu Feb 02 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.0-1
-       Adding latest version to handle following CVEs
-       CVE-2016-7922, CVE-2016-7923, CVE-2016-7924, CVE-2016-7925,
-       CVE-2016-7926, CVE-2016-7927, CVE-2016-7928, CVE-2016-7929,
-       CVE-2016-7930, CVE-2016-7931, CVE-2016-7932, CVE-2016-7933,
-       CVE-2016-7934, CVE-2016-7935, CVE-2016-7936, CVE-2016-7937,
-       CVE-2016-7938, CVE-2016-7939, CVE-2016-7940, CVE-2016-7973,
-       CVE-2016-7974, CVE-2016-7975, CVE-2016-7983, CVE-2016-7984,
-       CVE-2016-7985, CVE-2016-7986, CVE-2016-7992, CVE-2016-7993,
-       CVE-2016-8574, CVE-2016-8575, CVE-2017-5202, CVE-2017-5203,
-       CVE-2017-5204, CVE-2017-5205, CVE-2017-5341, CVE-2017-5342,
-       CVE-2017-5482, CVE-2017-5483, CVE-2017-5484, CVE-2017-5485,
-       CVE-2017-5486
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.7.4-2
-	GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.7.4-1
-   Upgrade version.
*   Mon Apr 6  2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.7.3-1
-   Updating version to 4.7.3
