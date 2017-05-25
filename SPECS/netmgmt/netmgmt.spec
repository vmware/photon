Summary:       PhotonOS Network Management Utilities
Name:          netmgmt
Version:       1.1.0
Release:       3%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache2.0
URL:           http://www.vmware.com
Source0:       %{name}-%{version}.tar.gz
Patch0:        netmgmt-1.1.0-2.patch
Distribution:  Photon
BuildRequires: autoconf
BuildRequires: check >= 0.9.4
BuildRequires: docker >= 1.12
BuildRequires: glib-devel
Requires:      glib
Requires:      libgcc
Requires:      pcre
Requires:      systemd >= 228
%define sha1 netmgmt=d1e4b5700e7f3a6a6b674c9db41d4adfe5f54c00

%description
Network management utilities for PhotonOS

%package devel
Summary: netmgmt development headers and libraries
Group: Development/Libraries
Requires: netmgmt = %{version}-%{release}

%description devel
header files and libraries for netmgmt

%package cli-devel
Summary: netmgmt development cli headers and libraries
Group: Development/Libraries
Requires: netmgmt = %{version}-%{release}

%description cli-devel
header files and libraries for netmgmt cli

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

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig
# First argument is 1 => New Installation
# First argument is 2 => Upgrade

%files
%defattr(-,root,root)
%{_bindir}/netmgr
%{_lib64dir}/libnetmgr.so.*
%{_lib64dir}/libnetmgrcli.so.*

%files devel
%{_includedir}/netmgmt/netmgr.h
%{_lib64dir}/libnetmgr.a
%{_lib64dir}/libnetmgr.so

%files cli-devel
%{_includedir}/netmgmt/netmgrcli.h
%{_lib64dir}/libnetmgrcli.a
%{_lib64dir}/libnetmgrcli.so


# %doc ChangeLog README COPYING

%changelog
*    Thu  May 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-3
-    Fix handling of invalid match section config files.
*    Tue  Apr 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-2
-    Add query cfg filename API, remove fw_rule API, misc cleanup.
*    Fri  Mar 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-1
-    Update netmgmt to v1.1.0
*    Thu  Oct 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-3
-    Fix to allow reading multiple keys in a config section.
*    Tue  Aug 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-2
-    Fix DNS servers CLI bug.
*    Thu  Jul 28 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-1
-    Update DNS servers CLI and API.
*    Wed  Jul 20 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.3-2
-    Allow ini-parser to read and carry keys with empty values.
*    Fri  Jul 08 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.3-1
-    Update set/get dns_servers, duid, iaid APIs.
*    Wed  Jun 15 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-5
-    Fix linklist delete bug in iniparser.
*    Fri  Jun 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-4
-    Set correct file permissions for config files.
*    Wed May 25 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-3
-    Do not fail if valid commands are executed
*    Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-2
-    GA - Bump release of all rpms
*    Wed May 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-1
-    Initial
