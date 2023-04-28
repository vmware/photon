Summary:        software font engine.
Name:           freetype2
Version:        2.13.0
Release:        1%{?dist}
License:        BSD/GPL
URL:            http://www.freetype.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.gz
%define sha512  freetype=0d2bfc3980313e1578b69568394666e1721c11dfdb47f21cb46ced48d0afcc674e175391ee0f64ffbcee814cded2d9a8fe6273029253c1adf642078ac8c0dd73
BuildRequires:  libtool
BuildRequires:  zlib-devel
BuildRequires:  glibc
BuildRequires:  pkg-config
BuildRequires:  bash

%description
FreeType is a software font engine that is designed to be small, efficient, highly customizable, and portable while capable of producing high-quality output (glyph images). It can be used in graphics libraries, display servers, font conversion tools, text image generation tools, and many other products as well.

%package        devel
Summary:        Header and development files
Requires:       freetype2 = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -n freetype-%{version} -p1

%build
%configure --with-harfbuzz=no
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
make %{?_smp_mflags} -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.13.0-1
- Upgrade to v2.13.0
* Fri May 06 2022 Tapas Kundu <tkundu@vmware.com> 2.10.2-4
- Fix CVE-2022-27404, CVE-2022-27405 and CVE-2022-27406
* Thu Feb 17 2022 Tapas Kundu <tkundu@vmware.com> 2.10.2-3
- Fix CVE-2020-15999
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.10.2-2
- Fix build with new rpm
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 2.10.2-1
- Automatic Version Bump
* Wed Sep 12 2018 Sujay G <gsujay@vmware.com> 2.9.1-1
- Version bump to 2.9.1
* Thu Jun 14 2018 Tapas Kundu <tkundu@vmware.com> 2.7.1-4
- CVE-2018-6942
* Mon May 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.1-3
- CVE-2017-8287
* Fri Apr 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-2
- CVE-2017-7857, CVE-2017-7858 and CVE-2017-7864
* Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-1
- Initial version
