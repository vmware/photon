Summary:        A network performance benchmark tool.
Name:           iperf
Version:        3.1
Release:        1%{?dist}
License:        GPL
URL:            https://github.com/esnet/iperf
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
#Source download URL: https://github.com/esnet/iperf/archive/3.1.tar.gz
Source0:        https://github.com/esnet/iperf/archive/%{name}-%{version}.tar.gz
Patch1:         disablepg.patch
%define sha1 iperf=0e00ce535b02b869b53649ef50fc1516a49c858c
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
%setup -q
%patch1 -p1

%build
echo "VDBG optflags: " %{optflags}
./bootstrap.sh
./configure \
        CFLAGS="%{optflags}" \
        CXXFLAGS="%{optflags}" \
        --disable-silent-rules \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --datadir=%{_datarootdir} \
        --sysconfdir=/etc
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install

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
*       Wed Oct 28 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-1
-       Add iperf v3.1 package.
