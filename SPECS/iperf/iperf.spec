Summary:        A network performance benchmark tool.
Name:           iperf
Version:        3.19
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/esnet/iperf
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

#Source download URL: https://github.com/esnet/iperf/archive/%{version}.tar.gz
Source0:        https://github.com/esnet/iperf/archive/%{name}-%{version}.tar.gz
%define sha512 iperf=f0631cd1158a90dc402fa30563e6f26dbdbc5d5b0665bed25248f9153118f55296913abeb89bf0b1db760ca2c68f60e0c9cf2df82aa096318ca618ca09176388

Patch1:         disablepg.patch

BuildRequires:  autoconf
BuildRequires:  automake

%description
ipref is a network performance measurement tool that can measure the maximum
achievable network bandwidth on IP networks. It supports tuning of various
parameters related to timing, protocols, and buffers.  For each test it
reports the bandwidth, loss, and other parameters.

%package        doc
Summary:        Documentation for iperf
%description    doc
It contains the documentation and manpages for iperf package.
Requires:       %{name} = %{version}-%{release}

%prep
%autosetup -p1

%build
echo "VDBG optflags: " %{optflags}
./bootstrap.sh
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/iperf3
%{_includedir}/iperf_api.h
%{_libdir}/libiperf.*

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/iperf3.1.gz
%{_mandir}/man3/libiperf.3.gz

%changelog
* Mon May 19 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 3.19-1
- Update to v3.19, fixes CVE-2024-26306, CVE-2024-53580
* Tue Apr 2 2024 Roye Eshed <roye.eshed@broadcom.com> 3.16-1
- Update iperf version to 3.16 and absorb CVE-2023-7250 fix
* Fri Aug 11 2023 Roye Eshed <eshedr@vmware.com> 3.14-1
- Update iperf version and absorb CVE-2023-38403 fix
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.9-2
- Bump up release for openssl
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.9-1
- Automatic Version Bump
* Mon Jun 22 2020 Ankit Jain <ankitja@vmware.com> 3.8.1-1
- Automatic Version Bump
* Wed Sep 05 2018 Ankit Jain <ankitja@vmware.com> 3.6-1
- Upgraded to version 3.6
* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.1.7-1
- Upgraded to version 3.1.7
* Thu Oct 6 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.3-1
- Upgraded to version 3.1.3
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.1.2-1
- Upgrade to 3.1.2
* Wed Oct 28 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-1
- Add iperf v3.1 package.
