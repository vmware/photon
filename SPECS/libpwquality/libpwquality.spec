%global build_if %{photon_subrelease} >= 91

# Default off, but overridable from pkg_build_options.json / rpmbuild -D.
# A plain define of STIG_HARDEN here would win over -D and make every
# STIG conditional in this spec permanently unreachable, and untested.
%{!?STIG_HARDEN: %global STIG_HARDEN 0}

Summary:        It provides common functions for password quality checking
Name:           libpwquality
Version:        1.4.4
Release:        10%{?dist}
URL:            https://github.com/libpwquality/libpwquality
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/libpwquality/libpwquality/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2

%if 0%{?STIG_HARDEN}
Source1: default-pwquality.conf
%endif

Source2: license.txt
%include %{SOURCE2}

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
    --with-python-binary=%{python3} \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?STIG_HARDEN}
install -vDm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/security/pwquality.conf
%endif

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
%{python3_sitearch}/pwquality-*.egg-info/*
%{python3_sitearch}/*.so

%changelog
* Mon Aug 31 2026 Daniel Casota <dcasota@gmail.com> 1.4.4-10
- Replace the plain define of STIG_HARDEN with a define-if-unset so the flag
  can be set from pkg_build_options.json or rpmbuild -D. A plain define in the
  spec body beats -D, so every STIG conditional in this spec was unreachable
  and had never been parsed or built in any constellation.
- No change to the default build: with STIG_HARDEN unset the value is still 0
  and the expanded spec is identical.
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.4.4-9
- Extended to build for subrelease 91 and above
* Tue Dec 09 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.4-8
- Bump up release as part of python3 upgrade
* Fri Nov 14 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.4-7
- Revert STIG hardening changes
* Fri Oct 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.4-6
- Harden pwquality by default
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.4.4-5
- Release bump for SRP compliance
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
