Summary:        ALSA library
Name:           alsa-lib
Version:        1.2.3.2
Release:        4%{?dist}
License:        LGPLv2+
URL:            http://alsa-project.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.alsa-project.org/files/pub/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=1fbc6360fda841bd9ca488739bdc9f4142c1b4a07ff767f48f1e160e3d4dff914aed422c97088e238b5e77d7e30aa79ff72569c3348a4cf4a412e1e4bce0bf2a

Patch0: CVE-2026-25068.patch

%description
The ALSA Library package contains the ALSA library used by programs
(including ALSA Utilities) requiring access to the ALSA sound interface.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
rm %{buildroot}%{_libdir}/*.la

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*
%exclude %dir %{_libdir}/debug
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Mon Feb 02 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.3.2-4
- Fix CVE-2026-25068
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.3.2-3
- Exclude debug symbols properly
* Mon Jul 20 2020 Tapas Kundu <tkundu@vmware.com> 1.2.3.2-2
- Build with python3
- Mass removal python2
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.3.2-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace
