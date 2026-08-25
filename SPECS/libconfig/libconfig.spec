%global build_if %{photon_subrelease} >= 91

Summary:       C/C++ configuration file library
Name:          libconfig
Version:       1.8.2
Release:       3%{?dist}
URL:           http://www.hyperrealm.com/libconfig
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/hyperrealm/libconfig/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Requires: libgcc
Requires: libstdc++

BuildRequires: texinfo

%description
Libconfig is a simple library for processing structured configuration files,
like this one: test.cfg. This file format is more compact and more readable than XML.
And unlike XML, it is type-aware, so it is not necessary to do string parsing in application code.

%package devel
Summary: Development headers for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
%{summary}

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

rm -r %{buildroot}%{_libdir}/*.la \
      %{buildroot}%{_infodir}/dir

%if 0%{?with_check}
%check
%make_build check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libconfig*.so.15*

%files devel
%defattr(-,root,root)
%{_includedir}/libconfig*
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc
%{_libdir}/cmake/libconfig++/libconfig++Config.cmake
%{_libdir}/cmake/libconfig/libconfigConfig.cmake
%{_infodir}/libconfig.info*

%changelog
* Mon Aug 17 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.2-3
- Add texinfo to BuildRequires
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.8.2-2
- Extend to build for 91 and above
* Thu Jun 18 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.2-1
- Upgrade to v1.8.2
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
