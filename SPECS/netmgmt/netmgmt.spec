Summary:       PhotonOS Network Management Utilities
Name:          netmgmt
Version:       1.0.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache2.0
URL:           http://www.vmware.com
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: autoconf
BuildRequires: glibc-devel
Requires:      glibc
%define sha1 netmgmt=0c399954f74e092a0e935478218113447641d0a2

%description
Network management utilities for PhotonOS

%package devel
Summary: netmgmt development headers and libraries
Group: Development/Libraries
Requires: netmgmt=%{version}-%{release}

%description devel
header files and libraries for netmgmt 

%prep
%setup -q

%build
autoreconf -mif
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_lib64dir}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%files
%defattr(-,root,root)
%{_bindir}/netmgr
%{_lib64dir}/libnetmgr.so*

%files devel
%{_lib64dir}/libnetmgr.a

# %doc ChangeLog README COPYING

%changelog
*   Tue May 17 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.0-1
-   Initial
