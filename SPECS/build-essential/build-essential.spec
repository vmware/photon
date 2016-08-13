Name:           build-essential
Summary:        This package is meant to install all build tools
Version:        0.1
Release:        1%{?dist}
License:        GPLv2
Requires:       gcc, binutils, make, glibc-devel, linux-api-headers, automake, autoconf, libtool, gawk, binutils, util-linux-devel

%description
This package is meant to install all build tools

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
*   Fri Aug 5 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.1-1
-   Initial
