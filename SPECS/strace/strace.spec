Summary:  Tracks system calls that are made by a running process
Name:     strace
Version:  4.26
Release:  1%{?dist}
License:  BSD
URL:      https://strace.io/
Group:    Development/Debuggers
Vendor:   VMware, Inc.
Distribution: Photon
Source0:  https://strace.io/files/%{version}/%{name}-%{version}.tar.xz
%define sha1 strace=b4a054adb74563fc121bcd19b158f58955a20a33
BuildRequires:  libacl-devel, libaio-devel

%description
The strace program intercepts and displays the system calls made by a running process. strace also records
all the arugments and return values from the system calls. This is useful in debugging a process.

%package graph
Summary:  strace graph
Group:    System Environment/Security
Requires: %{name} = %{version}-%{release}
%description graph
The strace graph is perl script , It displays a graph of invoked subprocesses, and is useful for finding out what complex commands do

%prep
%setup -q

%build
%ifarch aarch64
%configure \
  --disable-mpers \
%else
%configure
%endif

# to resolve build issue with glibc-2.26
sed -i 's/struct ucontext/ucontext_t/g' linux/x86_64/arch_sigreturn.c
sed -i 's/struct ucontext/ucontext_t/g' linux/arm/arch_sigreturn.c

make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}

%check
make -k check

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
*   Wed Jan 06 2021 Susant Sahani <ssahani@vmware.com> 4.26-1
-   Seperate strace-graph to remove perl dependency
-   Version bump
*   Tue Nov 13 2018 Srinidhi Rao <srinidhir@vmware.com> 4.25-1
-   Updating to version 4.25
*   Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 4.24-2
-   Fix 4.24 for aarch64
*   Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 4.24-1
-   Updating to version 4.24
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.16-3
-   Aarch64 support
*   Wed Aug 23 2017 Alexey Makhalov <amakhalov@vmware.com> 4.16-2
-   Fix compilation issue for glibc-2.26
*   Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.16-1
-   Update to version 4.16
*   Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11-3
-   Exclude perl dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.11-1
-   Upgrade version.
*   Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 4.10-1
-   Initial build. First version
