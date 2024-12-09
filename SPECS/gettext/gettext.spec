Summary:        Utilities for internationalization and localization
Name:           gettext
Version:        0.22
Release:        1%{?dist}
URL:            http://www.gnu.org/software/gettext
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz
%define sha512  gettext=c6368344aa4e0f6fd7c4a93023a5f7b377c7bb97b8ea688fd54f4c385c069d9ff27611d8763b1aed6328b6d3c4db7b34bd89bfbf6525ecaef11eb58434a4d4fa

Source1: license.txt
%include %{SOURCE1}

Requires: libgcc
Requires: libstdc++
Requires: %{name}-libs = %{version}-%{release}

%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.

%package devel
Summary: Development files for %{name}
# autopoint is GPLv3+
# libasprintf is LGPLv2+
# libgettextpo is GPLv3+
License: LGPL-2.0-or-later and GPL-3.0-or-later and GFDL-1.2-or-later
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: xz
Requires: diffutils

%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.

%package libs
Summary: Libraries for %{name}
# libasprintf is LGPLv2+
# libgettextpo is GPLv3+
License: LGPL-2.0-or-later and GPL-3.0-or-later

%description libs
This package contains libraries used internationalization support.

%prep
%autosetup -p1

%build
%configure \
    --docdir=%{_docdir}/%{name}-%{version} \
    --disable-silent-rules \
    --disable-static \
    --enable-shared \
    --without-emacs

%make_build

%install
%make_install
rm -rf %{buildroot}%{_docdir}/gettext-%{version}/examples \
       %{buildroot}%{_infodir}

%find_lang %{name} --all-name

%if 0%{?with_check}
%check
sed -i 's/test-term-ostream-xterm.sh//1' ./libtextstyle/tests/Makefile
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/%{name}/*
%{_datadir}/%{name}/*
%{_datadir}/%{name}-%{version}/*

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/libgettextlib-0.*.so
%{_libdir}/libgettextsrc-0.*.so

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%exclude %{_libdir}/libgettextlib-0.*.so
%exclude %{_libdir}/libgettextsrc-0.*.so
%{_includedir}/*
%{_datadir}/aclocal/*
%{_mandir}/*
%{_docdir}/*

%changelog
* Mon Dec 09 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.22-1
- Version bump.
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.21.1-3
- Release bump for SRP compliance
* Fri Jun 14 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 0.21.1-2
- Fix CVE-2016-3709/2019-19956/2021-3517/2021-3518/
- 2021-3541/2022-23308/2022-40303/2022-40304/2024-25062
* Thu Jan 12 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.21.1-1
- Update to version 0.21.1
* Mon Nov 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 0.21-2
- Fix make check
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 0.21-1
- Automatic Version Bump
* Thu Jun 18 2020 Ashwin H <ashwinh@vmware.com> 0.19.8.1-3
- Fix CVE-2018-18751
* Thu Nov 08 2018 Alexey Makhalov <amakhalov@vmware.com> 0.19.8.1-2
- Cross compilation support
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 0.19.8.1-1
- Update to version 0.19.8.1
* Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 0.19.8-1
- Upgrade to 0.19.8
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.19.5.1-2
- GA - Bump release of all rpms
* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 0.19.5.1-1
- Updated to version 0.19.5.1
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 0.18.3.2-2
- Handled locale files with macro find_lang
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 0.18.3.2-1
- Initial build. First version
