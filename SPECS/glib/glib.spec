Summary:       Low-level libraries useful for providing data structure handling for C.
Name:          glib
Version:       2.68.4
Release:       2%{?dist}
License:       LGPLv2+
URL:           https://developer.gnome.org/glib/
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       http://ftp.acc.umu.se/pub/gnome/sources/glib/2.68/glib-%{version}.tar.xz
%define sha512 glib=be17d79b41d17fd2b144184d6e793180667b7d9ba299215ea6d4948b4c05f6d888b4868c48643e25935a34ee2f85ee1d03e53325151b7a61819437cbd3c84b10
Source1:       additional.patches
BuildRequires: pcre-devel
BuildRequires: libffi-devel
BuildRequires: pkg-config
BuildRequires: which
BuildRequires: python3-xml
BuildRequires: python3
BuildRequires: python3-libs
BuildRequires: util-linux-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: gtk-doc
BuildRequires: meson
Requires:      elfutils-libelf
Requires:      pcre-libs
Requires:      libffi
Provides:      pkgconfig(glib-2.0)
Provides:      pkgconfig(gmodule-2.0)
Provides:      pkgconfig(gmodule-no-export-2.0)
Provides:      pkgconfig(gobject-2.0)
Provides:      pkgconfig(gio-2.0)
Provides:      pkgconfig(gio-unix-2.0)
Provides:      pkgconfig(gthread-2.0)

# CVE fixes
%include %{SOURCE1}

# Fix for CVE-2024-34397 [100..117]
# Backported following Upstream MRs:
# https://gitlab.gnome.org/GNOME/glib/-/merge_requests/4040
# https://gitlab.gnome.org/GNOME/glib/-/merge_requests/4056
# Added a supporting patch to add 'g_set_str()' API:
# https://gitlab.gnome.org/GNOME/glib/-/commit/49ae9b490d12f79d51d04a27daed9a8e01c65758
Patch100: 0001-gdbusmessage-Cache-the-arg0-value.patch
Patch101: 0002-tests-Add-a-data-driven-test-for-signal-subscription.patch
Patch102: 0003-tests-Add-support-for-subscribing-to-signals-from-a-.patch
Patch103: 0004-tests-Add-a-test-case-for-what-happens-if-a-unique-n.patch
Patch104: 0005-tests-Add-test-coverage-for-signals-that-match-the-m.patch
Patch105: 0006-gdbusprivate-Add-symbolic-constants-for-the-message-.patch
Patch106: 0007-gdbusconnection-Move-SignalData-SignalSubscriber-hig.patch
Patch107: 0008-gdbusconnection-Factor-out-signal_data_new_take.patch
Patch108: 0009-gdbusconnection-Factor-out-add_signal_data.patch
Patch109: 0010-gdbusconnection-Factor-out-remove_signal_data_if_unu.patch
Patch110: 0011-gdbusconnection-Stop-storing-sender_unique_name-in-S.patch
Patch111: 0012-gdbus-Track-name-owners-for-signal-subscriptions.patch
Patch112: 0013-gdbusconnection-Don-t-deliver-signals-if-the-sender-.patch
Patch113: 0014-tests-Add-a-test-for-matching-by-two-well-known-name.patch
Patch114: 0015-tests-Add-a-test-for-signal-filtering-by-well-known-.patch
Patch115: 0016-tests-Ensure-that-unsubscribing-with-GetNameOwner-in.patch
Patch116: 0001-strfuncs-add-g_set_str.patch
Patch117: 0001-gdbusconnection-Allow-name-owners-to-have-the-syntax.patch

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

%description devel
Static libraries and header files for the support library for the glib library

%package  schemas
Summary:  gsettings schemas compiling tool
Group:    Development/Libraries
Requires: glib = %{version}-%{release}

%description    schemas
Gsettings schemas compiling tool

%package   doc
Summary:   Documentation for Glib
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The glib-doc package includes documentation for the GLib library.

%prep
%autosetup -p1

%build
%meson \
    -Dman=true \
    -Dselinux=disabled \
    -Dgtk_doc=true

%meson_build

%install
%meson_install

%post    -p /sbin/ldconfig
%postun    -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libglib-*.so.*
%{_libdir}/libgthread-*.so.*
%{_libdir}/libgmodule-*.so.*
%{_libdir}/libgio-*.so.*
%{_libdir}/libgobject-*.so.*

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
%exclude %{_datadir}/gtk-doc/*

%files schemas
%defattr(-, root, root)
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_datadir}/glib-2.0/schemas/*

%files doc
%defattr(-, root, root)
%doc %{_datadir}/gtk-doc/html/*

%changelog
* Tue Jun 04 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 2.68.4-2
- Fixes CVE-2024-34397
* Mon Sep 25 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.68.4-1
- Fix misc CVEs from issue 3126
- Fix CVE-2023-32643 which is a side effect of 3126
- Update to 2.68.4 to match CVE fixes
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
