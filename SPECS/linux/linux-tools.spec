Summary:      This package contains the 'perf' performance analysis tools for Linux kernel 
Name:         linux-tools
Version:      4.2.8
Release:      1%{?dist}
License:      GPLv2
URL:          http://www.kernel.org/
Group:        System/Tools
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=b97bee7c8db5c4da53e754b8bad8ff9646016a73
Requires:         filesystem kmod coreutils binutils

%description
This package contains the 'perf' performance analysis tools for Linux kernel. 

%prep
%setup -q -n linux-%{version}

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
%{_libdir}
%{_bindir}
/etc/bash_completion.d/* 

%changelog
*   Thu Mar 10 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.8-1
-   Upgrading kernel version to 4.2.8
*	Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-2
-	Fix for new perl
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version

