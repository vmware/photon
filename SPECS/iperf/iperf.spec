Summary:        A network performance benchmark tool.
Name:           iperf
Version:        3.17.1
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/esnet/iperf
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
#Source download URL: https://github.com/esnet/iperf/archive/3.8.1.tar.gz
Source0:        https://github.com/esnet/iperf/archive/%{name}-%{version}.tar.gz
Patch1:         disablepg.patch
%define sha512  iperf=54789c5a63081aa803575ce1df3cb251a3b0bb16313f049f2479ae3a5af39944ace1222d4a086bed0ab34821da73371b2499f8b8283791a953d861da4cfc56f0
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
*       Tue May 14 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 3.17.1-1
-       Update to version 3.17.1
*       Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 3.12-1
-       Automatic Version Bump
*       Sun May 29 2022 Gerrit Photon <photon-checkins@vmware.com> 3.11-1
-       Automatic Version Bump
*       Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.9-2
-       Bump up release for openssl
*       Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.9-1
-       Automatic Version Bump
*       Mon Jun 22 2020 Ankit Jain <ankitja@vmware.com> 3.8.1-1
-       Automatic Version Bump
*       Wed Sep 05 2018 Ankit Jain <ankitja@vmware.com> 3.6-1
-       Upgraded to version 3.6
*       Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.1.7-1
-       Upgraded to version 3.1.7
*       Thu Oct 6 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.3-1
-       Upgraded to version 3.1.3
*       Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-2
-       GA - Bump release of all rpms
*       Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.1.2-1
-       Upgrade to 3.1.2
*       Wed Oct 28 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-1
-       Add iperf v3.1 package.
