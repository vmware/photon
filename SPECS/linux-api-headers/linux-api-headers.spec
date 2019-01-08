Summary:	Linux API header files
Name:		linux-api-headers
Version:	4.19.13
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution: Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=ddf3c474b5c86113bd1cfdc1fd8dfda7918a6b5b
BuildArch:	noarch
%description
The Linux API Headers expose the kernel's API for use by Glibc.
%prep
%setup -q -n linux-%{version}
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
*   Tue Jan 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.13-1
-   Update to version 4.19.13
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
