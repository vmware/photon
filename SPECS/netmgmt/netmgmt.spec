Summary:       PhotonOS Network Management Utilities
Name:          netmgmt
Version:       1.0.3
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache2.0
URL:           http://www.vmware.com
Source0:       %{name}-%{version}.tar.gz
Patch0:        netmgmt-v103-iniparser-allow-empty-keyvalue.patch
Distribution:  Photon
BuildRequires: autoconf
BuildRequires: glib-devel
Requires:      glib
Requires:      systemd >= 228
%define sha1 netmgmt=c81f2226cac089a1d79d118ecca7f0a2ef873140

%description
Network management utilities for PhotonOS

%package devel
Summary: netmgmt development headers and libraries
Group: Development/Libraries
Requires: netmgmt = %{version}-%{release}

%description devel
header files and libraries for netmgmt 

%prep
%setup -q
%patch0 -p1

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
%{_includedir}/*
%{_lib64dir}/libnetmgr.a

# %doc ChangeLog README COPYING

%changelog
*	Wed  Jul 20 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.3-2
-	Allow ini-parser to read and carry keys with empty values.
*	Fri  Jul 08 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.3-1
-	Update set/get dns_servers, duid, iaid APIs.
*	Wed  Jun 15 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-5
-	Fix linklist delete bug in iniparser.
*	Fri  Jun 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-4
-	Set correct file permissions for config files.
*	Wed May 25 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-3
-	Do not fail if valid commands are executed
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-2
-	GA - Bump release of all rpms
*   Wed May 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-1
-   Initial
