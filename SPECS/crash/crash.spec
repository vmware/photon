Name:          crash
Version:       7.1.5
Release:       2%{?dist}
Summary:       kernel crash analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles
Group:         Development/Tools
Vendor:	       VMware, Inc.
Distribution:  Photon
URL:           http://people.redhat.com/anderson/
Source0:       http://people.redhat.com/anderson/crash-%{version}.tar.gz
%define sha1 crash=dd6b6f9e6aed648bdac4550d9d81442896dc98fd
%define CRASH_GCORE_VERSION	1.3.1
Source1:       http://people.redhat.com/anderson/extensions/crash-gcore-command-1.3.1.tar.gz
%define sha1 crash-gcore=9f1a889ad7b3f01c88866dac44cabddd7d35f99c
License:       GPL
Patch0:        gcore-support-linux-4.4.patch
BuildRequires: binutils
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
Requires:      binutils
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

%package devel
Group:         Development/Libraries
Summary:       Libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

This package contains libraries and header files need for development.

%prep
%setup -q -n %{name}-%{version}
%setup -a 1
cd crash-gcore-command-%{CRASH_GCORE_VERSION}
%patch0 -p1

%build
make RPMPKG=%{version}-%{release}
cd crash-gcore-command-%{CRASH_GCORE_VERSION}
make -f gcore.mk ARCH=SUPPORTED TARGET=X86_64

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
mkdir -p %{buildroot}%{_bindir}
%make_install
mkdir -p %{buildroot}%{_mandir}/man8
install -pm 644 crash.8 %{buildroot}%{_mandir}/man8/crash.8
mkdir -p %{buildroot}%{_includedir}/crash
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash
mkdir -p %{buildroot}%{_libdir}/crash
install -pm 755 crash-gcore-command-%{CRASH_GCORE_VERSION}/gcore.so %{buildroot}%{_libdir}/crash/

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%{_bindir}/crash
%{_libdir}/crash/gcore.so
%{_mandir}/man8/crash.8.gz
%doc COPYING3 README

%files devel
%defattr(-,root,root)
%dir %{_includedir}/crash
%{_includedir}/crash/*.h

%changelog
*   Fri Oct 07 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-2
-   gcore-support-linux-4.4.patch
*   Fri Sep 30 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-1
-   Update version to 7.1.5 (it supports linux-4.4)
-   Added gcore plugin
-   Remove zlib-devel requirement from -devel subpackage
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.1.4-2
-   GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 7.1.4-1
-   Updated to version 7.1.4
*   Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 7.1.3-1
-   Initial build. First version
