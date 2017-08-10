Summary:	Linux API header files
Name:		linux-api-headers
Version:	4.4.81
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution: Photon
Source0:    	http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=b13679a3a9fc9f38c67bdbe321b426e3f19373ad
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
*   Fri Aug 11 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.81-1
-   Version update
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.74-1
-   Update version
*   Wed Jun 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.71-1
-   Update version
*   Thu May 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.70-1
-   Update version
*   Tue May 9 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.67-1
-   Update version
*   Tue May 2 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.65-1
-   Update version
*   Thu Apr 27 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.64-1
-   Update version
*   Mon Apr 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.60-1
-   Update to linux-4.4.60
*   Wed Mar 15 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.54-1
-   Update to linux-4.4.54
*   Thu Feb 23 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.51-1
-   Update to linux-4.4.51
*   Mon Jan 9 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.41-1
-   Update to linux-4.4.41
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
