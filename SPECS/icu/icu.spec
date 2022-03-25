Summary:    International Components for Unicode.
Name:       icu
Version:    67.1
Release:    2%{?dist}
License:    MIT and UCD and Public Domain
URL:        http://www.icu-project.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://download.icu-project.org/files/%{name}4c/%{version}/%{name}4c-67_1-src.tgz
%define sha1 %{name}=6822a4a94324d1ba591b3e8ef084e4491af253c1

%description
The International Components for Unicode (ICU) package is a mature, widely used set of C/C++ libraries providing Unicode and Globalization support for software applications.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1 -n %{name}/source

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%exclude %{_libdir}/%{name}
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 67.1-2
- Exclude debug symbols properly
* Tue Oct 13 2020 Ashwin H <ashwinh@vmware.com> 67.1-1
- update to 67.1
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 61.1-1
- Update to latest version
* Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 55.1-1
- Initial build for photon
