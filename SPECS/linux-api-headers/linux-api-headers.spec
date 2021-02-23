Summary:	Linux API header files
Name:		linux-api-headers
Version:	4.9.258
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution: Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=4cb67679baa0c8dd301245647072477b21aca679
BuildArch:	noarch
Patch0:         Implement-the-f-xattrat-family-of-functions.patch
%description
The Linux API Headers expose the kernel's API for use by Glibc.
%prep
%setup -q -n linux-%{version}
%patch0 -p1
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
*   Tue Feb 23 2021 Sharan Turlapati <sturlapati@vmware.com> 4.9.258-1
-   Update to version 4.9.258
*   Wed Jan 20 2021 Keerthana K <keerthanak@vmware.com> 4.9.252-1
-   Update to version 4.9.252
*   Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.9.249-1
-   Update to version 4.9.249
*   Mon Dec 14 2020 Vikash Bansal <bvikas@vmware.com> 4.9.248-1
-   Update to version 4.9.248
*   Tue Nov 24 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.246-1
-   Update to version 4.9.246
*   Wed Nov 11 2020 Keerthana K <keerthanak@vmware.com> 4.9.243-1
-   Update to version 4.9.243
*   Mon Nov 02 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-1
-   Update to version 4.9.241
*   Mon Oct 19 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.240-1
-   Update to version 4.9.240
*   Thu Oct 01 2020 Ankit Jain <ankitja@vmware.com> 4.9.237-1
-   Update to version 4.9.237
*   Mon Sep 14 2020 Vikash Bansal <bvikas@vmware.com> 4.9.236-1
-   Update to version 4.9.236
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.9.228-1
-   Update to version 4.9.228
*   Mon Jun 08 2020 Vikash Bansal <bvikas@vmware.com> 4.9.226-1
-   Update to version 4.9.226
*   Fri May 22 2020 Ajay Kaher <akaher@vmware.com> 4.9.224-1
-   Update to version 4.9.224
*   Tue May 05 2020 ashwin-h <ashwinh@vmware.com> 4.9.221-1
-   Update to version 4.9.221
*   Thu Apr 30 2020 ashwin-h <ashwinh@vmware.com> 4.9.220-1
-   Update to version 4.9.220
*   Mon Apr 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.219-1
-   Update to version 4.9.219
*   Mon Mar 23 2020 Keerthana K <keerthanak@vmware.com> 4.9.217-1
-   Update to version 4.9.217
*   Tue Mar 17 2020 Ajay Kaher <akaher@vmware.com> 4.9.216-1
-   Update to version 4.9.216
*   Tue Mar 03 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.9.214-1
-   Update to version 4.9.214
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.210-1
-   Update to version 4.9.210
*   Wed Dec 04 2019 Ajay Kaher <akaher@vmware.com> 4.9.205-1
-   Update to version 4.9.205
*   Tue Nov 19 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.202-1
-   Update to version 4.9.202
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.201-1
-   Update to version 4.9.201
*   Thu Nov 07 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.199-1
-   Update to version 4.9.199
*   Mon Oct 21 2019 Ajay Kaher <akaher@vmware.com> 4.9.197-1
-   Update to version 4.9.197
*   Wed Sep 18 2019 bvikas <bvikas@vmware.com> 4.9.193-1
-   Update to version 4.9.193
*   Mon Aug 12 2019 Alexey Makhalov <amakhalov@vmware.com> 4.9.189-1
-   Update to version 4.9.189
*   Thu Jul 11 2019 VIKASH BANSAL <bvikas@vmware.com> 4.9.185-1
-   Update to version 4.9.185
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.182-1
-   Update to version 4.9.182
*   Mon Jun 03 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.180-1
-   Update to version 4.9.180
*   Fri May 24 2019 srinidhira0 <srinidhir@vmware.com> 4.9.178-1
-   Update to version 4.9.178
*   Wed May 08 2019 Ajay Kaher <akaher@vmware.com> 4.9.173-1
-   Update to version 4.9.173
*   Fri Apr 05 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.168-1
-   Update to version 4.9.168
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.166-1
-   Update to version 4.9.166
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.163-1
-   Update to version 4.9.163
*   Mon Feb 04 2019 Ajay Kaher <akaher@vmware.com> 4.9.154-1
-   Update to version 4.9.154
*   Mon Nov 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.140-1
-   Update to version 4.9.140
*   Fri Nov 16 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.137-1
-   Update to version 4.9.137
*   Mon Oct 01 2018 srinidhira0 <srinidhir@vmware.com> 4.9.130-1
-   Update to version 4.9.130
*   Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.124-1
-   Update to version 4.9.124
*   Fri Aug 17 2018 Bo Gan <ganb@vmware.com> 4.9.120-1
-   Update to version 4.9.120
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.118-1
-   Update to version 4.9.118
*   Mon Jul 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.116-1
-   Update to version 4.9.116
*   Mon Jul 23 2018 srinidhira0 <srinidhir@vmware.com> 4.9.114-1
-   Update to version 4.9.114
*   Sat Jul 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.111-1
-   Update to version 4.9.111
*   Thu Jun 21 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-1
-   Update to version 4.9.109
*   Mon May 21 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.101-2
-   Add the f*xattrat family of syscalls.
*   Mon May 21 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.101-1
-   Update to version 4.9.101
*   Wed May 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.99-1
-   Update to version 4.9.99
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.98-1
-   Update to version 4.9.98
*   Mon Apr 30 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.97-1
-   Update to version 4.9.97
*   Mon Apr 23 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.94-2
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Wed Apr 18 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.94-1
-   Update to version 4.9.94
*   Mon Apr 02 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.92-1
-   Update to version 4.9.92
*   Tue Mar 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.90-1
-   Update to version 4.9.90
*   Thu Mar 22 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.89-1
-   Update to version 4.9.89
*   Mon Feb 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.80-1
-   Update to version 4.9.80
*   Wed Jan 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.79-1
-   Update version to 4.9.79
*   Fri Jan 26 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.78-1
-   Update version to 4.9.78.
*   Tue Jan 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-1
-   Version update
*   Thu Dec 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.71-1
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
