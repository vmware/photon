Summary:       C/C++ configuration file library
Name:          libconfig
Version:       1.7.3
Release:       2%{?dist}
License:       LGPLv2
URL:           http://www.hyperrealm.com/libconfig
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=3749bf9eb29bab0f6b14f4fc759f0c419ed27a843842aaabed1ec1fbe0faa8c93322ff875ca1291d69cb28a39ece86d512aec42c2140d566c38c56dc616734f4

%description
Libconfig is a simple library for processing structured configuration files,
like this one: test.cfg. This file format is more compact and more readable than XML.
And unlike XML, it is type-aware, so it is not necessary to do string parsing in application code.

%package devel
Summary:    Development files for libconfig
Requires:   %{name} = %{version}-%{release}

Conflicts: %{name} < 1.7.3-2%{?dist}

%description devel
Development libraries and headers for developing software with
libconfig.

%prep
%autosetup -p1

%build
autoreconf -vfi
%configure --disable-static

%make_build

%install
%make_install %{?_smp_flags}

rm -rf %{buildroot}%{_infodir}/dir

%check
%make_build test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/%{name}*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc
%{_infodir}/%{name}.info*
%exclude %{_libdir}/cmake/*

%changelog
* Tue Sep 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.7.3-2
- Introduce deve sub package
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.3-1
- Automatic Version Bump
* Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.2-1
- Automatic Version Bump
* Mon Jul 20 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.7-1
- Upgrade to version 1.7
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
- GA - Bump release of all rpms
* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.2-1
- Initial build.  First version.
