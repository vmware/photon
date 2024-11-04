Summary:    Check-0.12.0
Name:       check
Version:    0.15.2
Release:    3%{?dist}
URL:        https://github.com/libcheck/check
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution: Photon

Source0: https://github.com/libcheck/check/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=77fb34348bc1b1517801865afee5064121a245c10685e6bb6b8f743552646a0643cfdf9fd3dfbf9b2297d9430dfdd49616cf7daf41298d2dbd699f10d654a025

Source1: license.txt
%include %{SOURCE1}

Requires: gawk

%description
Check is a unit testing framework for C. It features a simple interface for defining unit tests,
putting little in the way of the developer. Tests are run in a separate address space,
so both assertion failures and code errors that cause segmentation faults or other signals can be caught.

%package devel
Summary:        Libraries and headers for developing programs with check
Requires:       %{name} = %{version}-%{release}

%description devel
Libraries and headers for developing programs with check

%prep
%autosetup -p1

%build
autoreconf --install
%configure
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
rm %{buildroot}%{_infodir}/dir

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_mandir}/man1/*
%{_infodir}/*
%{_docdir}/%{name}/*
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.15.2-3
- Release bump for SRP compliance
* Thu Sep 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.15.2-2
- Introduce devel subpackage
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 0.15.2-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 0.14.0-1
- Automatic Version Bump
* Thu Nov 08 2018 Alexey Makhalov <amakhalov@vmware.com> 0.12.0-2
- Cross compilation support
- Added required gawk
* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 0.12.0-1
- Upgraded to version 0.12.0
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.10.0-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 0.10.0-1
- Updated to version 0.10.0
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 0.9.14-2
- Updated group.
* Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.9.14-1
- Initial build. First version
