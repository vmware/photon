Name:       build-essential
Summary:    Metapackage to install all build tools
Version:    0.1
Release:    3%{?dist}
Group:      Development/Tools
License:    GPLv2
Vendor:     VMware, Inc.
Distribution:   Photon

Requires:   gcc
Requires:   binutils
Requires:   make
Requires:   glibc-devel
Requires:   linux-api-headers
Requires:   automake
Requires:   autoconf
Requires:   libtool
Requires:   gawk
Requires:   diffutils
Requires:   patch
Requires:   bison

%description
Metapackage to install all build tools

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
*   Fri Dec 07 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 0.1-3
-   Add patch and bison
*   Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> 0.1-2
-   Added diffutils
*   Fri Aug 5 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.1-1
-   Initial
