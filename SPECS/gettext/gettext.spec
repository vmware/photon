Summary:        Utilities for internationalization and localization
Name:           gettext
Version:        0.22.5
Release:        1%{?dist}
License:        GPL-3.0-or-later and LGPL-2.0-or-later and GFDL-1.2-or-later
URL:            http://www.gnu.org/software/gettext
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz
%define sha512 %{name}=a60999bb9d09441f138214d87acb7e59aab81e765bb9253a77c54902681c5de164a5a04de2a9778dfb479dbdefaab2d5de1fbaf6095c555c43e7e9fd7a1c09bd

Patch0:         libxml2-CVE-2016-3709.patch
Patch1:         libxml2-CVE-2019-19956.patch
Patch2:         libxml2-CVE-2021-3517.patch
Patch3:         libxml2-CVE-2021-3518.patch
Patch4:         libxml2-CVE-2021-3541.patch
Patch5:         libxml2-CVE-2022-23308.patch
Patch6:         libxml2-CVE-2022-40303.patch
Patch7:         libxml2-CVE-2022-40304.patch
Patch8:         libxml2-CVE-2024-25062.patch

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
# Using autosetup is not feasible
%setup -q -n gettext-%{version}

# Manually apply libxml2 patches instead of dynamically linking system installed libxml2 because its
# dependencies and their dynamic relocations have an impact on the startup time of a program that is linked with it

# Apply patches to gnulib-local/lib/libxml
pushd gnulib-local/lib/libxml
%autopatch -p1 -m0 -M8
popd

# Apply patches to gettext-tools/gnulib-lib/libxml
pushd gettext-tools/gnulib-lib/libxml
%autopatch -p1 -m0 -M8
popd

# Apply patches to libtextstyle/lib/libxml
pushd libtextstyle/lib/libxml
%autopatch -p1 -m0 -M8
popd

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
* Thu Jun 27 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 0.22.5-1
- Upgrade to v0.22.5
* Mon Aug 14 2023 Susant Sahani <ssahani@vmware.com> 0.22-1
- Version bump.
* Mon May 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.21.1-2
- Introduce deve & libs sub packages
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
