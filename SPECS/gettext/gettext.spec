Summary:        Utilities for internationalization and localization
Name:           gettext
Version:        0.21.1
Release:        3%{?dist}
URL:            http://www.gnu.org/software/gettext
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz
%define sha512  gettext=61e93bc9876effd3ca1c4e64ff6ba5bd84b24951ec2cc6f40a0e3248410e60f887552f29ca1f70541fb5524f6a4e8191fed288713c3e280e18922dd5bff1a2c9

Source1: license.txt
%include %{SOURCE1}

Patch0:         libxml2-CVE-2016-3709.patch
Patch1:         libxml2-CVE-2019-19956.patch
Patch2:         libxml2-CVE-2021-3517.patch
Patch3:         libxml2-CVE-2021-3518.patch
Patch4:         libxml2-CVE-2021-3541.patch
Patch5:         libxml2-CVE-2022-23308.patch
Patch6:         libxml2-CVE-2022-40303.patch
Patch7:         libxml2-CVE-2022-40304.patch
Patch8:         libxml2-CVE-2024-25062.patch

%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.

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
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-silent-rules
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/usr/share/doc/gettext-%{version}/examples
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
sed -i 's/test-term-ostream-xterm.sh//1' ./libtextstyle/tests/Makefile
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/gettext/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datarootdir}/aclocal/*
%{_datadir}/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*

%changelog
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
