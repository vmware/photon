Summary:     This package contains the 'perf' performance analysis tools for Linux kernel 
Name:        linux-tools
Version:    4.2.0
Release:    1%{?dist}
License:    GPLv2
URL:        http://www.kernel.org/
Group:        System/Tools
Vendor:        VMware, Inc.
Distribution: Photon
Source0:    http://www.kernel.org/pub/linux/kernel/v4.x/linux-4.2.tar.xz
%define sha1 linux=5e65d0dc94298527726fcd7458b6126e60fb2a8a
Requires:         filesystem kmod coreutils binutils

%description
This package contains the 'perf' performance analysis tools for Linux kernel. 

%prep
%setup -q -n linux-4.2

%build
cd tools/perf
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
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version

