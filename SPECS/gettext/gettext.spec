Summary:        Utilities for internationalization and localization
Name:           gettext
Version:        0.21
Release:        2%{?dist}
License:        GPLv3
URL:            http://www.gnu.org/software/gettext
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz
%define sha1    gettext=9d75b47baed1a612c0120991c4b6d9cf95e0d430

%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.

%prep
%setup -q

%build
%configure \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/usr/share/doc/gettext-%{version}/examples
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
sed -i 's/test-term-ostream-xterm.sh//1' ./libtextstyle/tests/Makefile
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

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
