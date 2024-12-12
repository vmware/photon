Summary:       Tracks system calls that are made by a running process
Name:          strace
Version:       6.1
Release:       2%{?dist}
URL:           https://strace.io/
Group:         Development/Debuggers
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://strace.io/files/%{version}/%{name}-%{version}.tar.xz
%define sha512 strace=3f0678d74c5c3e6b30c4dc4ed7ee4cb0829d3b7142dc014fcd887db3a68133bf7fedc623bae381dfe4305bd6cd15d4ca6776c6491009c2a053bb8c6ca1ae8e12

Source1: license.txt
%include %{SOURCE1}
BuildRequires: gcc gzip libacl-devel libaio-devel

%description
strace is a diagnostic, debugging and instructional userspace utility for Linux. It is
used to monitor and tamper with interactions between processes and the Linux kernel,
which include system calls, signal deliveries, and changes of process state.

%package       graph
Summary:       strace graph
Group:         System Environment/Security
Requires:      %{name} = %{version}-%{release}

%description   graph
The strace graph is perl script, It displays a graph of invoked subprocesses, and is
useful for finding out what complex commands do

%prep
%autosetup -p1

%build
%ifarch aarch64
%configure --disable-mpers
%else
%configure --enable-mpers=check
%endif

%make_build %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
%make_install %{?_smp_mflags}
cp src/strace-graph %{buildroot}%{_bindir}/

%check
make -k check %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/strace
%{_bindir}/strace-log-merge
%{_mandir}/man1/*

%files graph
%{_bindir}/strace-graph

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 6.1-2
- Release bump for SRP compliance
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 6.1-1
- Automatic Version Bump
* Thu Nov 24 2022 Susant Sahani <ssahani@vmware.com> 6.0-1
- Version Bump
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 5.19-1
- Automatic Version Bump
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 5.18-1
- Automatic Version Bump
* Tue Jan 12 2021 Susant Sahani <ssahani@vmware.com> 5.10-1
- Version Bump
* Tue Sep 22 2020 Harinadh D <hdommaraju@vmware.com> 4.21-2
- Seperate strace-graph to remove perl dependency
* Wed Jul 01 2020 Gerrit Photon <photon-checkins@vmware.com> 4.21-1
- Automatic Version Bump
* Tue Nov 13 2018 Srinidhi Rao <srinidhir@vmware.com> 4.25-1
- Updating to version 4.25
* Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 4.24-2
- Fix 4.24 for aarch64
* Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 4.24-1
- Updating to version 4.24
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.16-3
- Aarch64 support
* Wed Aug 23 2017 Alexey Makhalov <amakhalov@vmware.com> 4.16-2
- Fix compilation issue for glibc-2.26
* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.16-1
- Update to version 4.16
* Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11-3
- Exclude perl dependency
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11-2
- GA - Bump release of all rpms
* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.11-1
- Upgrade version.
* Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 4.10-1
- Initial build. First version
