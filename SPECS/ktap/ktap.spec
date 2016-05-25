# This package depends on exact version of kernel rpm
# since it provides kernel modules 
%define LINUX_VERSION 4.4.8

Summary: A New Scripting Dynamic Tracing Tool For Linux
Name:    ktap
Version: 0.4
Release: 3%{?dist}
License: GPLv2
URL: https://github.com/ktap/ktap
Source: %{name}-master.zip
%define sha1 ktap=8dca9a25e8917ad8cabdf176de487949c235ec80
Group:      Development/Tools
Vendor:     VMware, Inc.
Patch0:        linux-4.4-support.patch
Distribution:  Photon
BuildRequires: elfutils-devel
BuildRequires: linux-dev = %{LINUX_VERSION}
BuildRequires: linux = %{LINUX_VERSION}
BuildRequires: unzip
Requires: kmod
Requires: linux = %{LINUX_VERSION}

%description
ktap is a new scripting dynamic tracing tool for Linux, it uses a scripting language and lets users trace the Linux kernel dynamically. ktap is designed to give operational insights with interoperability that allows users to tune, troubleshoot and extend the kernel and applications. It's similar to Linux Systemtap and Solaris Dtrace.

%prep
%setup -q -n ktap-master
%patch0 -p1

%build
make ktap
# ugly hack: disable security hardening to build kernel module
# we need to remove sec hard specs file for that.
rm -f `dirname $(gcc --print-libgcc-file-name)`/../specs
make KVERSION=%{LINUX_VERSION} mod

%install
mkdir -p %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot} KVERSION=%{LINUX_VERSION}

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%files
%defattr(-, root, root, 0755)
%doc README.md
%{_bindir}/ktap
/lib/modules/%{LINUX_VERSION}/extra/ktapvm.ko

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  0.4-3
-	GA - Bump release of all rpms
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 0.4-2
-   Update to linux-4.4.8
*   Fri Dec 04 2015 Xiaolin Li <xiaolinl@vmware.com> 0.4-1
-   Initial build.  First version

