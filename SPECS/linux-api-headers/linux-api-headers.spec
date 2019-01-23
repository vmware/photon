Summary:	Linux API header files
Name:		linux-api-headers
Version:	4.4.171
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution: Photon
Source0:    	http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=0dad29240a55b758c2ebe81ce43b4766b7d81f7d
BuildArch:	noarch
# From SPECS/linux and used by linux-esx only
# It provides f*xattrat syscalls
Patch0:       Implement-the-f-xattrat-family-of-functions.patch
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
*   Thu Jan 24 2019 Ajay Kaher <akaher@vmware.com> 4.4.171-1
-   Update to version 4.4.171
*   Mon Nov 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.164-1
-   Update to version 4.4.164
*   Wed Nov 14 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.163-1
-   Update to version 4.4.163
*   Mon Oct 15 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.161-1
-   Update to version 4.4.161
*   Mon Sep 24 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.157-1
-   Update to version 4.4.157
*   Tue Sep 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.153-1
-   Update to version 4.4.153
*   Tue Aug 28 2018 Anish Swaminathan <anishs@vmware.com> 4.4.152-1
-   Update to version 4.4.152
*   Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.147-1
-   Update to version 4.4.147 to fix CVE-2018-12233.
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.146-1
-   Update to version 4.4.146
*   Mon Jul 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.145-1
-   Update to version 4.4.145
*   Thu Jul 26 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.144-1
-   Update to version 4.4.144
*   Mon Jul 16 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.140-1
-   Update to version 4.4.140
*   Tue Jul 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.139-1
-   Update to version 4.4.139
*   Mon Jun 25 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.138-1
-   Update to version 4.4.138
*   Wed Jun 13 2018 Alexey Makhalov <amakhalov@vmware.com> 4.4.137-1
-   Update to version 4.4.137
*   Mon May 21 2018 Bo Gan <ganb@vmware.com> 4.4.131-2
-   Sync with syscall number change for f*xattrat syscalls family
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.131-1
-   Update to version 4.4.131
*   Mon Apr 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.130-1
-   Update to version 4.4.130
*   Thu Apr 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.124-2
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Tue Mar 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.124-1
-   Update to version 4.4.124
*   Mon Feb 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.115-1
-   Update to version 4.4.115
*   Wed Jan 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.114-1
-   Update version to 4.4.114
*   Fri Jan 26 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.113-1
-   Update version to 4.4.113.
*   Tue Jan 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.109-1
-   Version update
*   Tue Dec 19 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.106-1
-   Version update
*   Fri Dec 08 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.104-1
-   Version update
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.103-1
-   Version update
*   Mon Nov 20 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.99-1
-   Version update
*   Tue Nov 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.96-1
-   Version update
*   Mon Oct 16 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.92-1
-   Version update
*   Fri Sep 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.88-1
-   Version update
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.86-1
-   Version update
*   Wed Aug 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.82-2
-   Implement the f*xattrat family of syscalls
*   Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.82-1
-   Version update
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
