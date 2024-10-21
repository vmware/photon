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

Patch0: fix-section-name-parsing-logic.patch
Patch1: 0001-destination-address-parsing-fix-in-case-of-ip-route.patch
Patch2: fix-dupe-string.patch

BuildRequires: autoconf
BuildRequires: check-devel
BuildRequires: docker >= 1.12
BuildRequires: glib-devel >= 2.68.4

Requires: glib >= 2.68.4
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
Requires: %{name} = %{version}-%{release}

%description devel
header files and libraries for netmgmt

%package cli-devel
Summary: netmgmt development cli headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description cli-devel
header files and libraries for netmgmt cli

%prep
%autosetup -p1

%build
autoreconf -mif
# fix gcc 9 compilation warning/error
CFLAGS="-O2 -g -Wno-error=format-truncation -Wno-error=restrict"
CFLAGS="${CFLAGS} -Wno-error=format-overflow -Wno-error=stringop-truncation"
CFLAGS="${CFLAGS} -Wno-error=stringop-overflow"
export CFLAGS

%configure \
    --libdir=%{_libdir} \
    --disable-static

%make_build
%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/netmgr
%{_libdir}/libnetmgr.so.*
%{_libdir}/libnetmgrcli.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/netmgr.h
%{_libdir}/libnetmgr.so

%files cli-devel
%defattr(-,root,root)
%{_includedir}/%{name}/netmgrcli.h
%{_libdir}/libnetmgrcli.so

%changelog
* Mon Oct 21 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.2.0-7
- Patched strstr issue in nm_space_delimited_string_append
* Fri Feb 02 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.2.0-6
- Patched for ip_route fix
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.2.0-5
- Bump version as part of glib upgrade
* Tue Oct 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-4
- Fix network file section name parsing logic
* Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-3
- Fix compilation issue with gcc-8.4.0
* Thu Jan 17 2019 Michelle Wang <michellew@vmware.com> 1.2.0-2
- Remove make check for netmgmt.
- Netmgmt tests are package tests instead of unit tests.
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
