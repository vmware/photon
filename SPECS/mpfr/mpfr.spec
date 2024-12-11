Summary:        Functions for multiple precision math
Name:           mpfr
Version:        4.1.0
Release:        3%{?dist}
URL:            http://www.mpfr.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=1bd1c349741a6529dfa53af4f0da8d49254b164ece8a46928cdb13a99460285622d57fe6f68cef19c6727b3f9daa25ddb3d7d65c201c8f387e421c7f7bee6273

Source1: license.txt
%include %{SOURCE1}

Requires:       gmp

%description
The MPFR package contains functions for multiple precision math.
%package devel
Summary:     Header and development files for mpfr
Requires:    %{name} = %{version}-%{release}

%description devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure \
      --enable-thread-safe \
      --docdir=%{_docdir}/%{name}-%{version} \
      --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libmpfr.so.*

%files devel
%{_includedir}/mpf2mpfr.h
%{_includedir}/mpfr.h
%{_libdir}/libmpfr.a
%{_libdir}/libmpfr.so
%{_libdir}/pkgconfig/*
%{_docdir}/mpfr-%{version}/NEWS
%{_docdir}/mpfr-%{version}/FAQ.html
%{_docdir}/mpfr-%{version}/examples/version.c
%{_docdir}/mpfr-%{version}/examples/rndo-add.c
%{_docdir}/mpfr-%{version}/examples/ReadMe
%{_docdir}/mpfr-%{version}/examples/sample.c
%{_docdir}/mpfr-%{version}/examples/divworst.c
%{_docdir}/mpfr-%{version}/examples/can_round.c
%{_docdir}/mpfr-%{version}/examples/threads.c
%{_docdir}/mpfr-%{version}/COPYING.LESSER
%{_docdir}/mpfr-%{version}/TODO
%{_docdir}/mpfr-%{version}/BUGS
%{_docdir}/mpfr-%{version}/AUTHORS
%{_docdir}/mpfr-%{version}/COPYING

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.1.0-3
- Release bump for SRP compliance
* Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 4.1.0-2
- Bump version to generate SRP provenance file
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 4.1.0-1
- Automatic Version Bump
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.2-1
- Automatic Version Bump
* Wed Sep 04 2019 Alexey Makhalov <amakhalov@vmware.com> 4.0.1-2
- Bump up release number to get generic mtune option from gmp.h
* Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.0.1-1
- Update package version
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 3.1.5-1
- Update package version
* Mon Oct 03 2016 ChangLee <changlee@vmware.com> 3.1.3-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.3-2
- GA - Bump release of all rpms
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.1.3-1
- Update version.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com>> 3.1.2-1
- Initial build. First version
