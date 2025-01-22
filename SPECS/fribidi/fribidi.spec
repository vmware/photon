Summary:        The FriBidi package is an implementation of the Unicode Bidirectional Algorithm (BIDI)
Name:           fribidi
Version:        1.0.9
Release:        3%{?dist}
License:        LGPLv2+
URL:            https://github.com/fribidi
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/fribidi/fribidi/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=e66989830941172fa003c8b9376719282fa1039592a1e158e975cab81ce8dcb2755453c64906a8464c047f9e9154e012d9bd37256b1f463e235648a13e4601ed

Patch0:         CVE-2022-25308.patch
Patch1:         CVE-2022-25309.patch
Patch2:         CVE-2022-25310.patch

BuildRequires:  meson

%description
The FriBidi package is an implementation of the Unicode Bidirectional Algorithm (BIDI)

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%meson \
       -Ddocs=false

%meson_build

%install
%meson_install

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

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
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.0.9-3
- Bump version as a part of meson upgrade
* Thu Mar 23 2023 Shivani Agarwal <shivania2@vmware.com> 1.0.9-2
- Fix CVE-2022-25308, CVE-2022-25309 and CVE-2022-25310
* Fri Aug 06 2021 Alexey Makhalov <amakhalov@vmware.com> 1.0.9-1
- Initial version
