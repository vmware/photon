Name:           build-essential
Summary:        Metapackage to install all build tools
Version:        0.1
Release:        2%{?dist}
License:        GPLv2
Requires:       gcc, binutils, make, glibc-devel, linux-api-headers, automake
Requires:       autoconf, libtool, gawk, diffutils, patch, bison

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
