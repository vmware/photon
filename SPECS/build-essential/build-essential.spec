Name:       build-essential
Summary:    Metapackage to install all build tools
Version:    0.1
Release:    5%{?dist}
Group:      Development/Tools
Vendor:     VMware, Inc.
URL:        https://github.com/vmware/photon
Distribution:   Photon

Source0: license.txt
%include %{SOURCE0}

Requires:   autoconf
Requires:   automake
Requires:   binutils
Requires:   bison
Requires:   diffutils
Requires:   file
Requires:   gawk
Requires:   gcc
Requires:   glibc-devel
Requires:   gzip
Requires:   linux-api-headers
Requires:   libtool
Requires:   make
Requires:   patch
Requires:   pkg-config
Requires:   tar

%description
Metapackage to install all build tools

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.1-5
-   Release bump for SRP compliance
*   Mon Jul 25 2022 Oliver Kurth <okurth@vmware.com> 0.1-4
-   Add file, gzip, pkg-config and tar
*   Fri Dec 07 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 0.1-3
-   Add patch and bison
*   Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> 0.1-2
-   Added diffutils
*   Fri Aug 5 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.1-1
-   Initial
