Summary: A New Scripting Dynamic Tracing Tool For Linux
Name:    ktap
Version: 0.4
Release: 7%{?kernelsubrelease}%{?dist}
License: GPLv2
URL: https://github.com/ktap/ktap
Source: %{name}-master.zip
%define sha1 ktap=8dca9a25e8917ad8cabdf176de487949c235ec80
Group:      Development/Tools
Vendor:     VMware, Inc.
Patch0:        linux-4.9-support.patch
Distribution:  Photon
BuildRequires: elfutils-devel
BuildRequires: linux-devel = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
BuildRequires: linux = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
BuildRequires: unzip
Requires: kmod
Requires: linux = %{KERNEL_VERSION}-%{KERNEL_RELEASE}

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
make KVERSION=%{KERNEL_VERSION}-%{KERNEL_RELEASE} mod

%install
mkdir -p %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot} KVERSION=%{KERNEL_VERSION}-%{KERNEL_RELEASE}

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%files
%defattr(-, root, root, 0755)
%doc README.md
%{_bindir}/ktap
/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra/ktapvm.ko

%changelog
*   Fri Jun 09 2017 Chang Lee <changlee@vmware.com> 0.4-7
-   Remove %check
*   Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> 0.4-6
-   Update to linux-4.9.0. Added support patch
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 0.4-5
-   Expand uname -r to have release number
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 0.4-4
-   Modified %check
*   Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 0.4-3
-   Added kernel macros
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4-3
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 0.4-2
-   Update to linux-4.4.8
*   Fri Dec 04 2015 Xiaolin Li <xiaolinl@vmware.com> 0.4-1
-   Initial build.  First version

