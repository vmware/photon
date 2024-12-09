Summary:        POSIX capability Library
Name:           libcap-ng
Version:        0.8.3
Release:        4%{?dist}
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://people.redhat.com/sgrubb/libcap-ng
Source0:        http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
%define sha512  libcap-ng=0ef9bc7bc6b7b59991f43b79aa6cde3e8d2c22c4b9ced2af8deae501e01d51e893033d109cb8aa0fdcba190140110993089245346334d7b114d18f1bb1b55b97

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  swig

%description
The libcap-ng library is intended to make programming with posix capabilities much easier
than the traditional libcap library. It includes utilities that can analyse all currently
running applications and print out any capabilities and whether or not it has an open ended
bounding set. An open bounding set without the securebits "NOROOT" flag will allow full
capabilities escalation for apps retaining uid 0 simply by calling execve.

%package  -n    python3-libcap-ng
Summary:        Python3 bindings for libaudit
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-libcap-ng
The python3-libcap-ng package contains the python3 bindings for libcap-ng.

%package        devel
Summary:        The libraries and header files needed for libcap-ng development.
Requires:       %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for libcap_ng development.

%prep
%autosetup

%build
%configure \
    --with-python3
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot} -name '*.la' -delete

%check
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

%ldconfig_scriptlets

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man8/*

%files -n python3-libcap-ng
%{python3_sitelib}/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_datadir}/aclocal/*.m4
%{_libdir}/*.a

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.8.3-4
- Release bump for SRP compliance
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.3-3
- Bump up version no. as part of swig upgrade
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.8.3-2
- Update release to compile with python 3.11
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 0.8.3-1
- Automatic Version Bump
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 0.8.2-2
- Use autosetup and ldconfig scriptlets
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 0.8.2-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 0.7.11-1
- Automatic Version Bump
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 0.7.10-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 0.7.9-3
- Mass removal python2
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 0.7.9-2
- Cross compilation support
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 0.7.9-1
- Updated to latest version
* Mon May 22 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.8-2
- Added python3 subpackage.
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 0.7.8-1
- Upgrade version to 0.7.8
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 0.7.7-3
- Moved man3 to devel subpackage.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.7-2
- GA - Bump release of all rpms
* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 0.7.7-1
- Initial version.
