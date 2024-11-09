Summary:      Low-level libraries useful for providing data structure handling for C.
Name:         glib
Version:      2.75.2
Release:      5%{?dist}
URL:          https://developer.gnome.org/glib/
Group:        Applications/System
Vendor:       VMware, Inc.
Distribution: Photon

Source0:  https://gitlab.gnome.org/GNOME/glib/-/releases/{version}/glib-%{version}.tar.xz
%define sha512  %{name}=f8e34d112c720e17fbc2325e5091f55d120cc82aa2a9012c6e9e3b81a969af97e501910f3f986fa305ab1abfbd77e69ee9c71bcdda33c6795c3b087e684272f6

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  pcre-devel
BuildRequires:  libffi-devel
BuildRequires:  pkg-config
BuildRequires:  which
BuildRequires:  python3-xml
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  util-linux-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  libselinux-devel
BuildRequires:  gtk-doc

Requires: elfutils-libelf
Requires: pcre-libs
Requires: libffi
Requires: libselinux

Provides: pkgconfig(glib-2.0)
Provides: pkgconfig(gmodule-2.0)
Provides: pkgconfig(gmodule-no-export-2.0)
Provides: pkgconfig(gobject-2.0)
Provides: pkgconfig(gio-2.0)
Provides: pkgconfig(gio-unix-2.0)
Provides: pkgconfig(gthread-2.0)

# CVE-2024-34397
# Upstream MR: https://gitlab.gnome.org/GNOME/glib/-/merge_requests/4040
Patch01: 0001-gdbusmessage-Cache-the-arg0-value.patch
Patch02: 0002-tests-Add-a-data-driven-test-for-signal-subscription.patch
Patch03: 0003-tests-Add-support-for-subscribing-to-signals-from-a-.patch
Patch04: 0004-tests-Add-a-test-case-for-what-happens-if-a-unique-n.patch
Patch05: 0005-tests-Add-test-coverage-for-signals-that-match-the-m.patch
Patch06: 0006-gdbusprivate-Add-symbolic-constants-for-the-message-.patch
Patch07: 0007-gdbusconnection-Move-SignalData-SignalSubscriber-hig.patch
Patch08: 0008-gdbusconnection-Factor-out-signal_data_new_take.patch
Patch09: 0009-gdbusconnection-Factor-out-add_signal_data.patch
Patch10: 0010-gdbusconnection-Factor-out-remove_signal_data_if_unu.patch
Patch11: 0011-gdbusconnection-Stop-storing-sender_unique_name-in-S.patch
Patch12: 0012-gdbus-Track-name-owners-for-signal-subscriptions.patch
Patch13: 0013-gdbusconnection-Don-t-deliver-signals-if-the-sender-.patch
Patch14: 0014-tests-Add-a-test-for-matching-by-two-well-known-name.patch
Patch15: 0015-tests-Add-a-test-for-signal-filtering-by-well-known-.patch
Patch16: 0016-tests-Ensure-that-unsubscribing-with-GetNameOwner-in.patch
Patch17: 0017-gdbus-proxy-test-Wait-before-asserting-name-owner-ha.patch
# Upstream MR to fix regression due to above MR 4040
# https://gitlab.gnome.org/GNOME/glib/-/merge_requests/4056
Patch18: 0001-gdbusconnection-Allow-name-owners-to-have-the-syntax.patch

%description
The GLib package contains a low-level libraries useful for providing data structure handling for C,
portability wrappers and interfaces for such runtime functionality as an event loop, threads,
dynamic loading and an object system. Development libs and headers are in glib-devel.

%package  devel
Summary:  Header files for the glib library
Group:    Development/Libraries
Requires: glib = %{version}-%{release}
Requires: python3-xml
Requires: pcre-devel
Requires: util-linux-devel
Requires: python3
Requires: libffi-devel
Requires: elfutils-libelf-devel
Requires: libselinux-devel

%description    devel
Static libraries and header files for the support library for the glib library

%package  schemas
Summary:  gsettings schemas compiling tool
Group:    Development/Libraries
Requires: glib

%description schemas
Gsettings schemas compiling tool

%prep
%autosetup -p1

%build
CONFIGURE_OPTS=(
    -Dlibelf=disabled
    -Dgtk_doc=false
    -Dtests=false
    -Dinstalled_tests=false
)

%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/libglib-*.so.*
%{_libdir}/libgthread-*.so.*
%{_libdir}/libgmodule-*.so.*
%{_libdir}/libgio-*.so.*
%{_libdir}/libgobject-*.so.*
%{_libexecdir}/gio-launch-desktop

%files devel
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/glib-*/*
%{_includedir}/*
%{_datadir}/*
%exclude %{_bindir}/glib-compile-schemas
%exclude %{_bindir}/gsettings
%exclude %{_datadir}/glib-2.0/schemas/*

%files schemas
%defattr(-, root, root)
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_datadir}/glib-2.0/schemas/*

%changelog
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.75.2-5
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.75.2-4
- Release bump for SRP compliance
* Tue Jun 04 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 2.75.2-3
- Fixes CVE-2024-34397
* Sat May 27 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.75.2-2
- Exclude duplicate packaged files
* Mon Jan 09 2023 Susant Sahani <ssahani@vmware.com> 2.75.2-1
- Update version
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.75.0-2
- Bump up due to change in elfutils
* Fri Nov 25 2022 Susant Sahani <ssahani@vmware.com> 2.75.0-1
- Update version
* Tue Nov 01 2022 Susant Sahani <ssahani@vmware.com> 2.74.1-1
- Update version
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.70.2-2
- Bump version as a part of libffi upgrade
* Mon Dec 13 2021 Susant Sahani <ssahani@vmware.com> 2.70.2-1
- Update to 2.70.2
* Mon Jul 19 2021 Susant Sahani <ssahani@vmware.com> 2.69.0-1
- Update to 2.69.0
* Fri Mar 26 2021 Ankit Jain <ankitja@vmware.com> 2.68.0-1
- Update to 2.68.0
* Fri Feb 26 2021 Ankit Jain <ankitja@vmware.com> 2.66.7-1
- Updated to 2.66.7 to fix CVE-2021-27218 and CVE-2021-27219
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.66.1-1
- Automatic Version Bump
* Mon Aug 24 2020 Keerthana K <keerthanak@vmware.com> 2.64.5-1
- Update to version 2.64.5
* Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 2.58.0-7
- Enabled gtk-doc
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 2.58.0-6
- Build with python3
- Mass removal python2
* Fri Aug 09 2019 Alexey Makhalov <amakhalov@vmware.com> 2.58.0-5
- Cross compilation support
* Tue Jul 09 2019 Ankit Jain <ankitja@vmware.com> 2.58.0-4
- Fix for CVE-2019-13012
* Mon Jun 03 2019 Ankit Jain <ankitja@vmware.com> 2.58.0-3
- Fix for CVE-2019-12450
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 2.58.0-2
- glib-devel requires python-xml.
* Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 2.58.0-1
- Update version to 2.58.0
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.52.1-2
- Requires pcre-libs, BuildRequires libffi-devel.
* Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 2.52.1-1
- Updated to version 2.52.1-1
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.48.2-2
- Modified %check
* Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.48.2-1
- Updated to version 2.48.2-1
* Thu Aug 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.6-3
- Update glib require for devel to use the same version and release
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.6-2
- GA - Bump release of all rpms
* Thu Apr 14 2016 Harish Udaiya Kumar<hudaiyakumar@vmware.com> 2.47.6-1
- Updated to version 2.47.6
* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 2.46.2-1
- Updated to version 2.46.2
* Fri Jun 12 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-3
- Added glib-schemas package
* Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-2
- Added more 'Provides: pkgconfig(...)' for base package
* Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 2.42.0-1
- Initial version
