Name:           build-essential
Summary:        Metapackage to install all build tools
Version:        0.1
Release:        2%{?dist}
License:        GPLv2
URL:            https://github.com/vmware/photon
Group:		    SystemUtilities
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       gcc
Requires:       binutils
Requires:       make
Requires:       glibc-devel
Requires:       linux-api-headers
Requires:       automake
Requires:       autoconf
Requires:       libtool
Requires:       gawk
Requires:       diffutils

%description
Metapackage to install all build tools

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
*   Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> 0.1-2
-   Added diffutils
*   Fri Aug 5 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.1-1
-   Initial
