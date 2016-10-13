Summary:      This package contains the 'perf' performance analysis tools for Linux kernel 
Name:         linux-tools
Version:      4.4.20
Release:      1%{?dist}
License:      GPLv2
URL:          http://www.kernel.org/
Group:        System/Tools
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=67f6d0f7d8c90d7f9fe7c3e1ee4d82b008b77767
Patch0:		  perf-top-sigsegv-fix.patch
Requires:         filesystem kmod coreutils binutils

%description
This package contains the 'perf' performance analysis tools for Linux kernel. 

%prep
%setup -q -n linux-%{version}
%patch0 -p1

%build
cd tools/perf
sed -i 's/EXTRA_WARNINGS += -Wnested-externs/#EXTRA_WARNINGS += -Wnested-externs/' ../scripts/Makefile.include
make 

%install
cd tools
make DESTDIR=%{buildroot} prefix=%{_prefix} perf_install 
mv %{buildroot}/usr/lib64 %{buildroot}%{_libdir}

%files
%defattr(-,root,root)
/usr/libexec
%exclude %{_libdir}/debug
%{_libdir}/traceevent
%{_bindir}
/etc/bash_completion.d/* 

%changelog
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update to linux-4.4.20
*   Mon Jun 20 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-3
-   Added patch to fix perf top segmentation fault. 
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-2
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
*   Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-2
-   Fix for new perl
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version

