Summary:	Utilities for block layer IO tracing
Name:		blktrace    
Version:	1.1.0
Release:	3%{?dist}
License:	GPLv2 
URL:		http://git.kernel.org/cgit/linux/kernel/git/axboe/blktrace.git/tree/README
Group:		Development/Tools/Other
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://blktrace.sourcearchive.com/downloads/1.1.0-2/%{name}_%{version}.orig.tar.bz2
%define sha1 blktrace=0a3a3203dbb5406098ad1d480d31d5104d4be823
Patch0:         blktrace-fix-CVE-2018-10689.patch
BuildRequires: libaio-devel
Requires:	libaio

%description
 blktrace is a block layer IO tracing mechanism which provides detailed
information about request queue operations up to user space.
%prep
%setup -q
%patch0 -p1

%build
make

%install
make install DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir}

%clean
rm -rf %{buildroot}/*
 
%files
%doc README 
%defattr(-,root,root)
%{_bindir}
%{_mandir}

%changelog
*   Mon Jul 23 2018 Keerthana K <keerthanak@vmware.com> 1.1.0-3
-   Fix for CVE-2018-10689.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.0-1
-   Updated to version 1.1.0
*   Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.5-1
-   Initial build.	First version
