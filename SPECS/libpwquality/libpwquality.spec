Summary:        It provides common functions for password quality checking
Name:           libpwquality
Version:        1.4.2
Release:        3%{?dist}
License:        BSD or GPLv2+
URL:            https://github.com/libpwquality/libpwquality
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/libpwquality/libpwquality/releases/download/libpwquality-%{version}/libpwquality-%{version}.tar.bz2
%define sha512 libpwquality=6f395e94797cc565edae6de8f4c7c60736d07ffa849c9878ec4d867f8cb7bea6f08bdd20501791dd05b02d487f8fea66a02a30841c7cea6e86b5903eaf685879

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
%autosetup -p1

%build
%configure \
        --with-securedir=%{_libdir}/security \
        --with-pythonsitedir=%{python3_sitearch} \
        --with-python-binary=%{__python3} \
        --disable-static
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

find %{buildroot} -name '*.la' -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/security/pwquality.conf
%{_libdir}/*.so.*
%{_libdir}/security/pam_pwquality.so
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
* Wed Jul 12 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.2-3
- Bump up to compile with python 3.10.11 & setuptools 65.5.1
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.2-2
- Bump up to compile with python 3.10
* Fri Sep 25 2020 Ankit Jain <ankitja@vmware.com> 1.4.2-1
- Initial version
