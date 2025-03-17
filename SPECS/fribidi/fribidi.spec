Summary:        GNU FriBidi is an implementation of the Unicode Bidirectional Algorithm (bidi).
Name:           fribidi
Version:        1.0.12
Release:        3%{?dist}
URL:            http://fribidi.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/fribidi/fribidi/releases/download/v%{version}/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  meson
BuildRequires:  ninja-build

%description
A library to handle bidirectional scripts (for example Hebrew, Arabic),
so that the display is done in the proper way; while the text data itself
is always written in logical order.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
Include files and libraries needed for developing applications which use
FriBidi.

%prep
%autosetup -p1

%build
%meson \
    -Ddocs=false

%meson_build

%install
%meson_install

%if 0%{?with_check}
%check
%meson_test
%endif

%clean
rm -rf %{buildroot}/*

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.0.12-3
- Bump version as a part of meson upgrade
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.0.12-2
- Release bump for SRP compliance
* Tue Nov 8 2022 Michelle Wang <michellew@vmware.com> 1.0.12-1
- Initial version. Required by pango-1.50.11.
