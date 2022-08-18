Summary:       Tracks system calls that are made by a running process
Name:          strace
Version:       5.19
Release:       1%{?dist}
License:       BSD
URL:           https://strace.io/
Group:         Development/Debuggers
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://strace.io/files/%{version}/%{name}-%{version}.tar.xz
%define sha512 strace=1ea1c6e12d05bf145bc3c74f8d06b08dfc3eae3a5a21bfe8ab080053dc4c2da8a95be5956652ea62bb083462015a55f9bc1d1023919dcf2929a05211b7dde963
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

make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} %{?_smp_mflags}
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
