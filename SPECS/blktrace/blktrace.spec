Summary:	Utilities for block layer IO tracing
Name:		blktrace
Version:	1.2.0
Release:	2%{?dist}
License:	GPLv2
URL:		http://git.kernel.org/cgit/linux/kernel/git/axboe/blktrace.git/tree/README
Group:		Development/Tools/Other
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://git.kernel.org/pub/scm/linux/kernel/git/axboe/blktrace.git/snapshot/%{name}-%{version}.tar.gz
%define sha1 blktrace=22a258ea65c6e826596b8e5a51e9c3f8bf758752
BuildRequires: libaio-devel
Requires:	libaio

%description
 blktrace is a block layer IO tracing mechanism which provides detailed
information about request queue operations up to user space.
%prep
%setup -q

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
*       Sun Sep 23 2018 Sujay G <gsujay@vmware.com>
-       Bump blktrace version to 1.2.0
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-2
-	GA - Bump release of all rpms
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.0-1
-   Updated to version 1.1.0
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.5-1
-	Initial build.	First version
