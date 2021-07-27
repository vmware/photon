%define debug_package %{nil}
Summary:	Linux API header files
Name:		linux-api-headers
Version:	5.10.52
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha1 linux=d1c6571f7fdf55939c451e35f02dd2cc7d143d14
BuildArch:	noarch
%description
The Linux API Headers expose the kernel's API for use by Glibc.
%prep
%autosetup -n linux-%{version}

%build
make %{?_smp_mflags} mrproper
%install
[ "%{_arch}" = "x86_64" ] && ARCH=x86_64
[ "%{_arch}" = "aarch64" ] && ARCH=arm64
[ "%{_arch}" = "i686" ] && ARCH=i386
cd %{_builddir}/linux-%{version}
make %{?_smp_mflags} ARCH=$ARCH headers_check
# 'make headers_install' needs rsync, but we would prefer not to add
# that dependency to linux-api-headers. So prepare the headers and
# copy them using 'cp' instead.
# make ARCH=$ARCH INSTALL_HDR_PATH=%{buildroot}%{_prefix} headers_install
make %{?_smp_mflags} ARCH=$ARCH headers
# Delete extraneous files, if any.
find usr/include -name '.*' -delete
rm usr/include/Makefile
mkdir -p %{buildroot}%{_prefix}
cp -r usr/include %{buildroot}%{_prefix}
find /%{buildroot}%{_includedir} \( -name .install -o -name ..install.cmd \) -delete
%files
%defattr(-,root,root)
%{_includedir}/*

%changelog
*   Mon Jul 26 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
-   Update to version 5.10.52
*   Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
-   Update to version 5.10.46
*   Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
-   Update to version 5.10.42
*   Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
-   Update to version 5.10.25
*   Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
-   Update to version 5.10.21
*   Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-1
-   Update to version 5.9.0
*   Wed Sep 30 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
-   Update to version 5.9.0-rc7
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
-   Update to version 4.19.127
*   Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
-   Update to version 4.19.112
*   Tue Feb 18 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
-   Update to version 4.19.104
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
-   Update to version 4.19.97
*   Mon Dec 09 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.87-2
-   Make it arch specific
*   Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
-   Update to version 4.19.87
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
-   Update to version 4.19.84
*   Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
-   Update to version 4.19.82
*   Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
-   Update to version 4.19.79
*   Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
-   Update to version 4.19.76
*   Wed Sep 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
-   Update to version 4.19.72
*   Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
-   Update to version 4.19.69
*   Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
-   Update to version 4.19.65
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
*   Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
-   Update to version 4.19.40
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
-   Update to version 4.19.32
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
-   Update to version 4.19.29
*   Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
-   Update to version 4.19.26
*   Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
-   Update to version 4.19.15
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
*   Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
-   Update to version 4.19.1
*   Thu Sep 20 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
-   Version update
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
*   Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
-   Version update
*   Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
-   Version update
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
-   Version update
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
-   Version update
*   Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
-   Version update
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   Version update
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Version update
*   Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
-   Version update
*   Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
-   Update to linux-4.9.27
*   Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
-   Update to linux-4.9.26
*   Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
-   Update to linux-4.9.24
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
-   Update to linux-4.4.35
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
-   Update to linux-4.4.31
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update kernel version to 4.4.20
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-2
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
*   Wed Dec 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
-   Upgrading kernel version to 4.2.0.
*   Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
-   Upgrading kernel version.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version
