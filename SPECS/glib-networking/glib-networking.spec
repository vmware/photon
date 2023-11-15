Summary:    Glib networking modules
Name:       glib-networking
Version:    2.59.1
Release:    6%{?dist}
License:    GPLv2
URL:        http://wiki.gnome.org/glib-networking
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://ftp.gnome.org/pub/GNOME/sources/glib-networking/2.50/%{name}-%{version}.tar.xz
%define sha512 %{name}=558fe6280394b8656464717c3962cf3e10c97e5cb1967f729809dcdd251b53cc2f775bbb308bb1dda951429480110c0f3b50fd8ba37c2088e169f790372b79bb

Patch0:     CVE-2020-13645.patch

BuildRequires:  nettle-devel
BuildRequires:  autogen-libopts-devel
BuildRequires:  libtasn1-devel
BuildRequires:  ca-certificates
BuildRequires:  gnutls-devel
BuildRequires:  openssl-devel
BuildRequires:  intltool
BuildRequires:  glib >= 2.58.3
BuildRequires:  glib-devel >= 2.58.3
BuildRequires:  glib-schemas
BuildRequires:  meson
BuildRequires:  gnome-common
BuildRequires:  ninja-build

Requires:   nettle
Requires:   gnutls
Requires:   libtasn1
Requires:   openssl
Requires:   ca-certificates

%description
Glib-netowkring contains networking related gio modules for Glib.

%package lang
Summary: Additional language files for glib-networking
Group: System Environment/Development
Requires: glib-networking
%description lang
These are the additional language files of glib-networking.

%prep
%autosetup -p1

%build
mkdir build && cd build
meson --prefix=%{_prefix} \
      -Dlibproxy_support=false \
      -Dgnome_proxy_support=false \
      -Dpkcs11_support=false ..

ninja

%install
cd build
DESTDIR=%{buildroot} ninja install
%find_lang %{name}

%check
%if 0%{?with_check}
cd build && ninja test
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
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.59.1-6
- Version bump due to glib change
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.59.1-5
- Exclude debug symbols properly
* Sat Apr 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.59.1-4
- Bump version as a part of nettle upgrade
* Fri Jun 05 2020 Ashwin H <ashwinh@vmware.com> 2.59.1-3
- Fix CVE-2020-13645
* Wed Aug 21 2019 Ashwin H <ashwinh@vmware.com> 2.59.1-2
- make check fix to work with RPMCHECK flag
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
