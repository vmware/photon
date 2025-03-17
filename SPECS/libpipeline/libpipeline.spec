Summary:    Library for manipulating pipelines
Name:       libpipeline
Version:    1.5.6
Release:    3%{?dist}
URL:        http://libpipeline.nongnu.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://download.savannah.gnu.org/releases/libpipeline/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%if 0%{?with_check}
BuildRequires:  check-devel
BuildRequires:  pkg-config
%endif

%description
Contains a library for manipulating pipelines of sub processes
in a flexible and convenient way.

%package devel
Summary:        Library providing headers and static libraries to libpipeline
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       pkgconfig(libpipeline)

%description devel
Development files for libpipeline

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

rm -f %{buildroot}%{_libdir}/*.la

%if 0%{?with_check}
%check
make -C tests check %{?_smp_mflags}
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.5.6-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.5.6-2
- Release bump for SRP compliance
* Thu Sep 29 2022 Gerrit Photon <photon-checkins@vmware.com> 1.5.6-1
- Automatic Version Bump
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.5-2
- Remove .la files
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.5.5-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.3-1
- Automatic Version Bump
* Tue Jul 07 2020 Shreenidhi Shedi <photon-checkins@vmware.com> 1.5.2-1
- Upgrade version to 1.5.2
* Mon Aug 19 2019 Shreenidhi Shedi <sshedi@vmware.com> 1.5.0-2
- Fix make check
* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.5.0-1
- Update to 1.5.0
- Split development files to devel package
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.1-2
- GA - Bump release of all rpms
* Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.1-1
- Initial build. First version
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.6-1
- Initial build. First version
