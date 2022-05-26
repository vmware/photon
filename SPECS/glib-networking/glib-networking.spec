Summary:      Glib networking modules
Name:         glib-networking
Version:      2.70.1
Release:      3%{?dist}
License:      GPLv2
URL:          http://wiki.gnome.org/glib-networking
Group:        System Environment/Development
Vendor:       VMware, Inc.
Distribution: Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/glib-networking/2.70.1/%{name}-%{version}.tar.xz
%define sha512 %{name}=a06b4df4481f95193f9ed4be6d39bbe9ecaf4de8e11a48750f7110d4cfa71aa56b7ec5b36af70b7128150447f1a39ce3aeadf71e2ac516f61708f1212f8f855d

Patch0: disable-pkcs-related-tests.patch

BuildRequires: nettle-devel
BuildRequires: autogen-libopts-devel
BuildRequires: libtasn1-devel
BuildRequires: ca-certificates
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
BuildRequires: intltool
BuildRequires: glib
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
Requires:   glib-networking

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

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%doc NEWS README
%{_libdir}/gio/modules/libgioopenssl.so
%{_libdir}/gio/modules/libgiognutls.so

%changelog
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
