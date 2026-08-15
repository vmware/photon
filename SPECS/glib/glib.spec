%global build_if %{photon_subrelease} >= 91

%define bootstrap   1

Summary:      Low-level libraries useful for providing data structure handling for C.
Name:         glib
Version:      2.89.2
Release:      2%{?dist}
URL:          https://developer.gnome.org/glib
Group:        Applications/System
Vendor:       VMware, Inc.
Distribution: Photon

Source0:  https://download.gnome.org/sources/glib/%{version}/glib-%{version}.tar.xz

%if 0%{?bootstrap}
%define introspection_version     1.86.0

Source1: gobject-introspection-%{introspection_version}.tar.xz
%endif

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  cmake
BuildRequires:  pcre2-devel
BuildRequires:  libffi-devel
BuildRequires:  pkg-config
BuildRequires:  python3-xml
BuildRequires:  python3-devel
BuildRequires:  util-linux-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  libselinux-devel
BuildRequires:  gtk-doc
BuildRequires:  zlib-devel

%if 0%{?bootstrap} == 0
%define ExtraBuildRequires gobject-introspection-devel
%else
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  autoconf-archive
%define ExtraBuildRequires glib-devel
%endif

Requires: elfutils-libelf
Requires: pcre2-libs
Requires: libffi
Requires: libselinux

Provides: pkgconfig(glib-2.0)
Provides: pkgconfig(gmodule-2.0)
Provides: pkgconfig(gmodule-no-export-2.0)
Provides: pkgconfig(gobject-2.0)
Provides: pkgconfig(gio-2.0)
Provides: pkgconfig(gio-unix-2.0)
Provides: pkgconfig(gthread-2.0)

%description
The GLib package contains a low-level libraries useful for providing data structure handling for C,
portability wrappers and interfaces for such runtime functionality as an event loop, threads,
dynamic loading and an object system. Development libs and headers are in glib-devel.

%package  devel
Summary:  Header files for the glib library
Requires: %{name} = %{version}-%{release}
Requires: python3-xml
Requires: pcre2-devel
Requires: util-linux-devel
Requires: python3
Requires: libffi-devel
Requires: elfutils-libelf-devel
Requires: libselinux-devel

%description    devel
Static libraries and header files for the support library for the glib library

%package  schemas
Summary:  gsettings schemas compiling tool
Requires: %{name} = %{version}-%{release}

%description schemas
Gsettings schemas compiling tool

%prep
# Using autosetup is not feasible
%setup -q
rm docs/reference/glib/*.svg \
   LICENSES/CC-BY-SA-3.0.txt

%build
CONFIGURE_OPTS=(
    -Ddocumentation=false
    -Dlibelf=disabled
    -Dtests=false
    -Dinstalled_tests=false
    -Ddefault_library=both
    -Ddtrace=disabled
    -Dsystemtap=disabled
    -Dsysprof=disabled
    -Dman-pages=disabled
    -Dintrospection=enabled
)

%if 0%{?bootstrap}
tar xf %{SOURCE1}

# Phase 1: build glib without introspection and install into the sandbox so
# gobject-introspection finds glib 2.88.0 (headers, .pc, .so) instead of
# the older system version (glib-devel is not in ExtraBuildRequires).
%set_build_flags
meson setup "${CONFIGURE_OPTS[@]/-Ddefault_library=both/-Ddefault_library=shared}" \
    -Dintrospection=disabled \
    --prefix /usr \
    . _build_bootstrap
ninja -C _build_bootstrap
DESTDIR=/ meson install -C _build_bootstrap --no-rebuild

# Phase 2: build gobject-introspection against the freshly-installed glib
pushd gobject-introspection-%{introspection_version}
%{meson} \
  -Dpython=%{python3} \
  -Dcairo=disabled \
  -Ddoctool=disabled

%{meson_build}
DESTDIR=/ meson install -C %{_vpath_builddir} --no-rebuild
popd
%endif

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
%{_libdir}/libgirepository-*.so.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.a
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
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.89.2-2
- Extend to build for 91 and above
* Fri Jul 24 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.89.2-1
- Upgrade to 2.89.2
* Mon Jun 01 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.88.0-5
- Migrate from pcre to pcre2
* Tue May 19 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.88.0-4
- Enable for 91 subrlease
* Fri Apr 10 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.88.0-3
- Enable introspection
* Mon Mar 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.88.0-2
- Remove unused docs dir
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.88.0-1
- Version upgrade
* Mon Feb 16 2026 Ajay Kaher <ajay.kaher@broadcom.com> 2.75.2-15
- Fix CVE-2026-0988, CVE-2026-1485, CVE-2026-1489
* Sun Feb 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.75.2-14
- Fix CVE-2026-1484
* Tue Jan 06 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.75.2-13
- Fix CVE-2025-14087, CVE-2025-14512
* Thu Dec 11 2025 Oliver Kurth <oliver.kurth@broadcom.com> 2.75.2-12
- add static library to -devel package
* Tue Dec 02 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.75.2-11
- Fix CVE-2025-13601
* Thu Nov 06 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.75.2-10
- Fix CVE-2025-4373
* Tue Aug 05 2025 Dweep Advani <dweep.advani@broadcom.com> 2.75.2-9
- Fix licenses
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.75.2-8
- Bump version as a part of meson upgrade
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.75.2-7
- Release bump for SRP compliance
* Mon Dec 09 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.75.2-6
- Fix CVE-2024-52533
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
