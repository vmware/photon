%global build_if %{photon_subrelease} <= 90

Summary:       C/C++ configuration file library
Name:          libconfig
Version:       1.7.3
Release:       2.1.0.2%{?dist}
URL:           http://www.hyperrealm.com/libconfig
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: texinfo

%description
Libconfig is a simple library for processing structured configuration files,
like this one: test.cfg. This file format is more compact and more readable than XML.
And unlike XML, it is type-aware, so it is not necessary to do string parsing in application code.

%prep
%autosetup -p1

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
* Mon Aug 17 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.3-2.1.0.2
- Add texinfo to BuildRequires
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.7.3-2.1.0.1
- Restrict to build for subrelease 90 and below
* Thu Jun 18 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.3-2.1
- Sub branch for 90 and 91
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
