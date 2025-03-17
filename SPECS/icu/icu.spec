Summary:        International Components for Unicode
Name:           icu
Version:        72.1
Release:        2%{?dist}
URL:            http://www.icu-project.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/unicode-org/icu/archive/refs/tags/%{name}4c-72_1-src.tgz

Source1: license.txt
%include %{SOURCE1}

%description
The International Components for Unicode (ICU) package is a mature,
widely used set of C/C++ libraries providing Unicode and Globalization support for software applications.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1 -n %{name}/source

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%exclude %dir %{_libdir}/debug
%exclude %{_libdir}/icu

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 72.1-2
- Release bump for SRP compliance
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 72.1-1
- Upgrade to v72.1
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 71.1-1
- Upgrade to v71.1
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 70.1-2
- Fix binary path
* Wed Nov 24 2021 Alexey Makhalov <amakhalov@vmware.com> 70.1-1
- Version update
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 69.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 67.1-1
- Automatic Version Bump
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 61.1-1
- Update to latest version
* Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 55.1-1
- Initial build for photon
