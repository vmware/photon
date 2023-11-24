Summary:      Glib networking modules
Name:         glib-networking
Version:      2.74.0
Release:      4%{?dist}
License:      GPLv2
URL:          http://wiki.gnome.org/glib-networking
Group:        System Environment/Development
Vendor:       VMware, Inc.
Distribution: Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/glib-networking/%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=f266c106f2c9379b95773a852c1b5c62ae1d6a758d25c436c3558f620d8e0a211201b3c4dfd89cdbe28b88430bba0cca621e62c01ea23d473983e203919bb1e6

Patch0: disable-pkcs-related-tests.patch

BuildRequires: nettle-devel
BuildRequires: autogen-libopts-devel
BuildRequires: libtasn1-devel
BuildRequires: ca-certificates
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
BuildRequires: intltool
BuildRequires: glib-devel
BuildRequires: glib-schemas
BuildRequires: meson
BuildRequires: gnome-common
BuildRequires: ninja-build
BuildRequires: systemd-rpm-macros

Requires:   nettle
Requires:   gnutls
Requires:   libtasn1
Requires:   openssl
Requires:   ca-certificates

%description
Glib-netowkring contains networking related gio modules for Glib.

%package    lang
Summary:    Additional language files for glib-networking
Group:      System Environment/Development
Requires:   %{name} = %{version}-%{release}

Conflicts:  %{name} < 2.74.0-2

%description lang
These are the additional language files of glib-networking.

%prep
%autosetup -p1

%build
CONFIGURE_OPTS=(
      -Dopenssl=enabled
      -Dgnutls=enabled
      -Dlibproxy=disabled
      -Dgnome_proxy=disabled
      -Dinstalled_tests=false
      -Dstatic_modules=false
)
%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install
%find_lang %{name}

%if 0%{?with_check}
%check
%meson_test
%endif

%files
%defattr(-,root,root)
%{_libdir}/gio/modules/libgioopenssl.so
%{_libdir}/gio/modules/libgiognutls.so
%{_libdir}/gio/modules/libgioenvironmentproxy.so

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Fri Nov 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.74.0-4
- Bump version as a part of gnutls upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.74.0-3
- Bump version as a part of openssl upgrade
* Wed May 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.74.0-2
- Package lang properly
* Tue Nov 01 2022 Susant Sahani <sshedi@vmware.com> 2.74.0-1
- Bump version
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.70.1-3
- Bump version as a part of gnutls upgrade
* Wed Aug 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.70.1-2
- Bump version as a part of nettle upgrade
* Mon Dec 13 2021 Susant Sahani <sshedi@vmware.com> 2.70.1-1
- Bump version
* Tue Aug 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.66.0-2
- Bump version as a part of nettle upgrade
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 2.66.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.64.3-2
- openssl 1.1.1
* Fri Sep 04 2020 Gerrit Photon <photon-checkins@vmware.com> 2.64.3-1
- Automatic Version Bump
* Wed Aug 19 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.59.1-2
- Bump version as a part of nettle-3.6 upgrade
* Wed Nov 21 2018 Ashwin H <ashwinh@vmware.com> 2.59.1-1
- Updated to 2.59.1 for make check fixes
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 2.58.0-1
- Update to version 2.58.0
* Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.50.0-1
- Updated to version 2.50.0
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.46.1-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.46.1-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 2.46.1-1
- Updating to new version.
* Wed Aug 12 2015 Touseef Liaqat <tliaqat@vmware.com> 2.45.1-1
- Initial build. First version
