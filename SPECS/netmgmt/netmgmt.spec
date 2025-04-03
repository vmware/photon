Summary:       PhotonOS Network Management Utilities
Name:          netmgmt
Version:       1.2.0
Release:       7%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache2.0
URL:           https://github.com/vmware/photonos-netmgr
Distribution:  Photon

Source0: https://github.com/vmware/photonos-netmgr/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=345c83eb8635d96c66d2926ae543ad872798036a3b68cd07f6c68d42537b71585692ce30f2537ec732143f506bac40e3e1a126aa19c8647627d6ca26899b74a8

Patch0: 0001-destination-address-parsing-fix-in-case-of-ip-route.patch
Patch1: fix-dupe-string.patch

BuildRequires: autoconf
BuildRequires: check >= 0.9.4
BuildRequires: docker >= 1.12
BuildRequires: glib-devel >= 2.58.3

Requires: glib >= 2.58.3
Requires: iputils
Requires: libgcc
Requires: ntp
Requires: pcre
Requires: systemd >= 228

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
%autosetup -p1

%build
autoreconf -mif
%configure \
        --libdir=%{_lib64dir}
%make_build

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

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

#%%doc ChangeLog README COPYING

%changelog
* Tue Apr 01 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.2.0-7
- Move nm_right_trim only if we have strings input
* Wed Mar 19 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.2.0-6
- Fix memory allocation
* Fri Dec 20 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.2.0-5
- Patched strstr issue in nm_space_delimited_string_append
* Mon Feb 05 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.2.0-4
- Patched for ip_route fix
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.2.0-3
- Version bump due to glib change
* Tue Sep 3 2019 Michelle Wang <michellew@vmware.com> 1.2.0-2
- Remove make check for netmgmt since those are package tests instead of unit tests.
* Thu Dec 06 2018 Michelle Wang <michellew@vmware.com> 1.2.0-1
- Update netmgmt to 1.2.0.
* Mon Oct 23 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-9
- Fix netmgr if_iaid CLI.
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-8
- Use standard configure macros
* Sat Oct 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-7
- Support netmgr for arm64.
* Wed Sep 20 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-6
- Backward compatibility interface.
* Sat Sep 09 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-5
- Retain current match conf when creating interface specific conf.
* Wed Aug 09 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-4
- Fix coverity issues.
* Thu May 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-3
- Fix handling of invalid match section config files.
* Tue Apr 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-2
- Add query cfg filename API, remove fw_rule API, misc cleanup.
* Fri Mar 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-1
- Update netmgmt to v1.1.0
* Thu Oct 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-3
- Fix to allow reading multiple keys in a config section.
* Tue Aug 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-2
- Fix DNS servers CLI bug.
* Thu Jul 28 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.4-1
- Update DNS servers CLI and API.
* Wed Jul 20 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.3-2
- Allow ini-parser to read and carry keys with empty values.
* Fri Jul 08 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.3-1
- Update set/get dns_servers, duid, iaid APIs.
* Wed Jun 15 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-5
- Fix linklist delete bug in iniparser.
* Fri Jun 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-4
- Set correct file permissions for config files.
* Wed May 25 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-3
- Do not fail if valid commands are executed
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-2
- GA - Bump release of all rpms
* Wed May 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-1
- Initial
