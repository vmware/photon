Summary:        Glib networking modules
Name:           glib-networking
Version:        2.66.0
Release:        8%{?dist}
License:        GPLv2
URL:            http://wiki.gnome.org/glib-networking
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnome.org/pub/GNOME/sources/glib-networking/2.50/%{name}-%{version}.tar.xz
%define sha512  %{name}=697798864746b40542873257a789290cacee425467e32c0eb096c87e124b37510753a990ef5d350f1db85c24da88e448bca9d8d8b4308123a74feac299176de5

BuildRequires:  nettle-devel
BuildRequires:  autogen-libopts-devel
BuildRequires:  libtasn1-devel
BuildRequires:  ca-certificates
BuildRequires:  gnutls-devel
BuildRequires:  openssl-devel
BuildRequires:  intltool
BuildRequires:  glib >= 2.68.4
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  glib-schemas
BuildRequires:  meson
BuildRequires:  gnome-common
BuildRequires:  ninja-build

Requires:       nettle
Requires:       gnutls
Requires:       libtasn1
Requires:       openssl
Requires:       ca-certificates

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
mkdir build &&
cd build &&
meson --prefix=%{_prefix}  \
      -Dlibproxy=disabled .. &&
ninja

%install
cd build
DESTDIR=%{buildroot} ninja install
%find_lang %{name}

%check
%if 0%{?with_check}
cd build
ninja test
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/gio/*
%exclude %dir %{_libdir}/debug

%files lang -f build/%{name}.lang
%defattr(-,root,root)

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.66.0-8
- Bump version as a part of meson upgrade
* Tue Nov 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.66.0-7
- Bump version as a part of gnutls upgrade
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.66.0-6
- Bump version as part of glib upgrade
* Fri Oct 28 2022 Michelle Wang <michellew@vmware.com> 2.66.0-5
- Update meson build parameters after meson bump up to 0.60.2
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.66.0-4
- Exclude debug symbols properly
* Tue Aug 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.66.0-3
- Bump version as a part of nettle upgrade
* Mon Apr 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.66.0-2
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
