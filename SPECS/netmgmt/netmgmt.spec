Summary:       PhotonOS Network Management Utilities
Name:          netmgmt
Version:       1.0.4
Release:       4%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache2.0
URL:           http://www.vmware.com
Source0:       %{name}-%{version}.tar.gz
Patch0:        netmgmt-v104-dns-buffer-overrun-fix.patch
Patch1:        netmgmt-v104-allow-multiple-keys.patch
Patch2:        netmgmt-set-duid-fix.patch
Distribution:  Photon
BuildRequires: autoconf
BuildRequires: glib-devel
Requires:      glib
Requires:      systemd >= 228
%define sha1 netmgmt=3e10acb9ce7d7697e571f999a75036eee5e156ea

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
%patch1 -p1
%patch2 -p1

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
*       Wed Nov 7 2018 Michelle Wang <michellew@vmware.com> 1.0.4-4
-       Fix set_duid for multi interface.
*	Thu  Oct 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-3
-	Fix to allow reading multiple keys in a config section.
*	Tue  Aug 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-2
-	Fix DNS servers CLI bug.
*	Thu  Jul 28 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-1
-	Update DNS servers CLI and API.
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
