Summary:        Thin layer of types for graphic libraries.
Name:           graphene
Version:        1.10.8
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/ebassi/graphene
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/ebassi/graphene/archive/refs/tags//%{name}-%{version}.tar.gz
%define sha512 %{name}=526b0c17049459b687ceb7f6c26c9d982535e4048e74a0b6282704f9811d3c2e7e0e6cfef166aa953306b6cf77add6677bc600ae0c66cc052dc04c3d0345bd68

BuildRequires:  meson >= 0.50
BuildRequires:  ninja-build
BuildRequires:  gobject-introspection-devel

Requires: gobject-introspection

%description
Graphene provides a small set of mathematical types needed to implement graphic
libraries that deal with 2D and 3D transformations and projections.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson \
      -Dtests=true \
      -Dinstalled_tests=false \
      %{nil}

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
%{_libdir}/girepository-1.0/
%{_libdir}/libgraphene-1.0.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/graphene-1.0/
%dir %{_libdir}/graphene-1.0
%{_libdir}/graphene-1.0/include/
%{_libdir}/libgraphene-1.0.so
%{_libdir}/pkgconfig/graphene-1.0.pc
%{_libdir}/pkgconfig/graphene-gobject-1.0.pc
%{_libexecdir}/installed-tests/*
%{_datadir}/gir-1.0/

%changelog
* Thu Sep 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10.8-2
- Fix devel package requires
* Mon Sep 5 2022 Shivani Agarwal <shivania2@vmware.com> 1.10.8-1
- Initial version
