Summary:        Packet Analyzer
Name:           tcpdump
Version:        4.99.1
Release:        1%{?dist}
License:        BSD
URL:            http://www.tcpdump.org
Source0:        http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
%define sha512  tcpdump=53d31355e1a6ef5a65bb3bf72454169fc80adf973a327a5768840e6ccf0550fbeb3c8a41f959635076d871df0619680321910a3a97879607f481cdaa8b7ceda7
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libpcap-devel
Requires:       libpcap

%description
Tcpdump is a common packet analyzer that runs under the command line.
It allows the user to display TCP/IP and other packets being
transmitted or received over a network to which the computer is attached.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%check
sed -i '626,636d' tests/TESTLIST
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/tcpdump
%{_bindir}/tcpdump.%{version}
%{_mandir}/man1/tcpdump.1.gz

%changelog
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 4.99.1-1
-   Automatic Version Bump
*   Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.9.3-4
-   Bump up release for openssl
*   Sun Nov 15 2020 Prashant S Chauhan <psinghchauha@vmware.com> 4.9.3-3
-   Added patch, fixes CVE-2020-8037
*   Wed Sep 30 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.9.3-2
-   openssl 1.1.1
*   Wed Oct 09 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 4.9.3-1
-   Update to version 4.9.3 to fix multiple CVEs
*   Thu Mar 14 2019 Michelle Wang <michellew@vmware.com> 4.9.2-2
-   Add patch CVE-2018-19519
*   Fri Sep 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.2-1
-   Updating version to 4.9.2
*   Thu Sep 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.1-2
-   Fix for CVE-2017-11541 CVE-2017-11542 and CVE-2017-11543
*   Thu Aug 03 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.1-1
-   Updating version to 4.9.1
*   Thu Feb 02 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.0-1
-   Adding latest version to handle following CVEs
-   CVE-2016-7922, CVE-2016-7923, CVE-2016-7924, CVE-2016-7925,
-   CVE-2016-7926, CVE-2016-7927, CVE-2016-7928, CVE-2016-7929,
-   CVE-2016-7930, CVE-2016-7931, CVE-2016-7932, CVE-2016-7933,
-   CVE-2016-7934, CVE-2016-7935, CVE-2016-7936, CVE-2016-7937,
-   CVE-2016-7938, CVE-2016-7939, CVE-2016-7940, CVE-2016-7973,
-   CVE-2016-7974, CVE-2016-7975, CVE-2016-7983, CVE-2016-7984,
-   CVE-2016-7985, CVE-2016-7986, CVE-2016-7992, CVE-2016-7993,
-   CVE-2016-8574, CVE-2016-8575, CVE-2017-5202, CVE-2017-5203,
-   CVE-2017-5204, CVE-2017-5205, CVE-2017-5341, CVE-2017-5342,
-   CVE-2017-5482, CVE-2017-5483, CVE-2017-5484, CVE-2017-5485,
-   CVE-2017-5486
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 4.7.4-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.7.4-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.7.4-1
-   Upgrade version.
*   Mon Apr 6  2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.7.3-1
-   Updating version to 4.7.3.
