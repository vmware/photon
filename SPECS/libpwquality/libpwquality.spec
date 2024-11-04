Summary:        It provides common functions for password quality checking
Name:           libpwquality
Version:        1.4.4
Release:        4%{?dist}
URL:            https://github.com/libpwquality/libpwquality
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/libpwquality/libpwquality/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
%define sha512  %{name}=2d49b79105361663f009f7183fde9123e6f1e63bd678dfe5418143f611e763af8dd44374b826b3c22a00e721047c539741dc44d99a2289b9ab229791768d6e76

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cracklib-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       cracklib
Requires:       Linux-PAM

%description
The libpwquality package provides common functions for password quality
checking and also scoring them based on their apparent randomness.
The library also provides a function for generating random passwords
with good pronounceability.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%package -n python3-pwquality
Summary:        Python bindings for the libpwquality library
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-pwquality
pwquality Python module that provides Python bindings
for the libpwquality library.

%prep
%autosetup

%build
%configure \
    --with-securedir=%{_libdir}/security \
    --with-pythonsitedir=%{python3_sitearch} \
    --with-python-binary=%{__python3} \
    --disable-static
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
find %{buildroot}%{python3_sitelib}/ -name '*.pyc' -delete -o \
    -name '*__pycache__' -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/security/pwquality.conf
%{_libdir}/*.so.*
%{_libdir}/security/pam_pwquality.so
%exclude %{_libdir}/libpwquality.la
%exclude %{_libdir}/security/pam_pwquality.la
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/locale/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files -n python3-pwquality
%defattr(-,root,root)
%{python3_sitearch}/pwquality-*.egg/*

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.4-4
- Release bump for SRP compliance
* Mon Jan 02 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.4.4-3
- Rebuild with new cracklib
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.4-2
- Bump up to compile with py311
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.4.4-1
- Automatic Version Bump
* Fri Sep 25 2020 Ankit Jain <ankitja@vmware.com> 1.4.2-1
- Initial version
