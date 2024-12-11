Summary:       C/C++ configuration file library
Name:          libconfig
Version:       1.7.3
Release:       2%{?dist}
URL:           http://www.hyperrealm.com/libconfig
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       %{name}-%{version}.tar.gz
%define sha512 %{name}=3749bf9eb29bab0f6b14f4fc759f0c419ed27a843842aaabed1ec1fbe0faa8c93322ff875ca1291d69cb28a39ece86d512aec42c2140d566c38c56dc616734f4

Source1: license.txt
%include %{SOURCE1}

%description
Libconfig is a simple library for processing structured configuration files,
like this one: test.cfg. This file format is more compact and more readable than XML.
And unlike XML, it is type-aware, so it is not necessary to do string parsing in application code.

%prep
%autosetup

%build
autoreconf -fi
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

rm -rf %{buildroot}%{_libdir}/*.la \
       %{buildroot}%{_infodir}/dir

%check
%if 0%{?with_check}
make test %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libconfig*.so.*
%{_includedir}/libconfig*
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc
%exclude %{_libdir}/cmake/libconfig++/libconfig++Config.cmake
%exclude %{_libdir}/cmake/libconfig/libconfigConfig.cmake
%{_infodir}/libconfig.info*

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.7.3-2
- Release bump for SRP compliance
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
