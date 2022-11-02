Summary:        opentype text shaping engine
Name:           harfbuzz
Version:        2.6.7
Release:        2%{?dist}
License:        MIT
URL:            http://harfbuzz.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.xz
%define sha512 %{name}=6fdd6e0952a73e1949349aa5416ef8fb3fc351b15c95be4fe1f341b111159fe58113b73a334db2697f4e3aaef5a761bd8f1d8964514406cad40f9862768d59de

BuildRequires:  glib-devel
BuildRequires:  freetype2-devel

Requires:       glib
Requires:       freetype2

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   glib-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/*

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake

%changelog
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.6.7-2
- Spec fixes
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.6.7-1
- Automatic Version Bump
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.9.0-1
- Update to version 1.9.0
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 1.4.5-2
- Add glib requirement
* Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.5-1
- Initial version
