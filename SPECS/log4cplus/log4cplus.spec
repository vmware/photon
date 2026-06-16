%global build_if %{photon_subrelease} >= 91

%define release_tag REL_2_1_2

Summary:        A simple to use C++23 logging API
Name:           log4cplus
Version:        2.1.2
Release:        2%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/log4cplus/log4cplus/wiki
Source0:        https://github.com/log4cplus/log4cplus/releases/download/%{release_tag}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
log4cplus is a simple to use C++ logging API providing thread-safe, flexible,
and arbitrarily granular control over log management and configuration.
It is modeled after the Java log4j API.

%package devel
Summary: development tools for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %name-devel package contains the libraries and header files
needed for development with %name.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_lib}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%changelog
* Mon Jun 15 2026 Bo Gan <bo.gan@broadcom.com> 2.1.2-2
- Regenerate license
* Wed Jun 03 2026 Bo Gan <bo.gan@broadcom.com> 2.1.2-1
- Initial packaging
