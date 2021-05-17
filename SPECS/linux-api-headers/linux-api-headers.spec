Summary:	Linux API header files
Name:		linux-api-headers
Version:	4.19.190
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=ce0796f609b4d6696ddc42a8969b3884f75e73bd

# Support for PTP_SYS_OFFSET_EXTENDED ioctl
Patch0:		0001-ptp-reorder-declarations-in-ptp_ioctl.patch
Patch1:		0002-ptp-add-PTP_SYS_OFFSET_EXTENDED-ioctl.patch
Patch2:		0003-ptp-deprecate-gettime64-in-favor-of-gettimex64.patch
Patch3:		0004-ptp-uapi-change-_IOW-to-IOWR-in-PTP_SYS_OFFSET_EXTEN.patch

BuildArch:	noarch
%description
The Linux API Headers expose the kernel's API for use by Glibc.
%prep
%setup -q -n linux-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make mrproper
make headers_check
%install
cd %{_builddir}/linux-%{version}
make INSTALL_HDR_PATH=%{buildroot}%{_prefix} headers_install
find /%{buildroot}%{_includedir} \( -name .install -o -name ..install.cmd \) -delete
%files
%defattr(-,root,root)
%{_includedir}/*
%changelog
*   Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 4.19.190-1
-   Update to version 4.19.190
*   Thu Apr 29 2021 Ankit Jain <ankitja@vmware.com> 4.19.189-1
-   Update to version 4.19.189
*   Tue Apr 13 2021 srinidhira0 <srinidhir@vmware.com> 4.19.186-1
-   Update to version 4.19.186
*   Mon Mar 22 2021 srinidhira0 <srinidhir@vmware.com> 4.19.182-1
-   Update to version 4.19.182
*   Fri Feb 26 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.177-1
-   Update to version 4.19.177
*   Tue Feb 09 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-1
-   Update to version 4.19.174
*   Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-1
-   Update to version 4.19.164
*   Tue Dec 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.163-1
-   Update to version 4.19.163
*   Tue Dec 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.160-3
-   Change PTP_SYS_OFFSET_EXTENDED IOCTL to _IOWR
*   Tue Dec 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.160-2
-   Add support for PTP_SYS_OFFSET_EXTENDED ioctl
*   Tue Nov 24 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-1
-   Update to version 4.19.160
*   Mon Nov 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-1
-   Update to version 4.19.154
*   Tue Oct 13 2020 Ajay Kaher <akaher@vmware.com> 4.19.150-1
-   Update to version 4.19.150
*   Mon Sep 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-1
-   Update to version 4.19.148
*   Tue Sep 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.145-1
-   Update to version 4.19.145
*   Sat Aug 08 2020 ashwin-h <ashwinh@vmware.com> 4.19.138-1
-   Update to version 4.19.138
*   Thu Jul 16 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-1
-   Update to version 4.19.132
*   Mon Jun 22 2020 Keerthana K <keerthanak@vmware.com> 4.19.129-1
-   Update to version 4.19.129
*   Fri Jun 05 2020 Vikash Bansal <bvikas@vmware.com> 4.19.126-1
-   Update to version 4.19.126
*   Wed May 27 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-1
-   Update to version 4.19.124
*   Mon Apr 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-1
-   Update to version 4.19.115
*   Mon Mar 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-1
-   Update to version 4.19.112
*   Tue Feb 18 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.104-1
-   Update to version 4.19.104
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
-   Update to version 4.19.97
*   Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
-   Update to version 4.19.87
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
-   Update to version 4.19.84
*   Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
-   Update to version 4.19.82
*   Thu Oct 17 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
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
