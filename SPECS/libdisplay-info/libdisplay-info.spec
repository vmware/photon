%global build_if %{photon_subrelease} >= 92

Summary:        EDID and DisplayID library
Name:           libdisplay-info
Version:        0.3.0
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Libraries
URL:            https://gitlab.freedesktop.org/emersion/libdisplay-info
Source0:        https://gitlab.freedesktop.org/emersion/libdisplay-info/-/archive/%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  hwdata

%description
An EDID and DisplayID library used by modern graphics stacks to parse monitor information.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/di-edid-decode
%{_libdir}/libdisplay-info.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/libdisplay-info/
%{_libdir}/libdisplay-info.so
%{_libdir}/pkgconfig/libdisplay-info.pc

%changelog
* Sat Mar 28 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 0.3.0-1
- Initial build for Mesa 25.3.x compatibility
