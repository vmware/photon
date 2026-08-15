%global build_if %{photon_subrelease} >= 91

Summary:        ALSA library
Name:           alsa-lib
Version:        1.2.8
Release:        7%{?dist}
URL:            http://alsa-project.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.alsa-project.org/files/pub/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2026-25068.patch
Patch1: CVE-2026-56109.patch

%description
The ALSA Library package contains the ALSA library used by programs
(including ALSA Utilities) requiring access to the ALSA sound interface.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name} < 1.2.8-5

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
%exclude %dir %{_libdir}/debug
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.2.8-7
- Extend to build for 91 and above
* Tue Aug 04 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.8-6
- Fix CVE-2026-56109
* Mon Jun 15 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 1.2.8-5
- Move pkgconfig .pc files to -devel subpackage
* Mon Feb 02 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.8-4
- Fix CVE-2026-25068
* Thu Aug 21 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.8-3
- Remove python3 from requires
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.2.8-2
- Release bump for SRP compliance
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.8-1
- Automatic Version Bump
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.7.2-1
- Automatic Version Bump
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.6.1-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.6.1-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.4-1
- Automatic Version Bump
* Mon Jul 20 2020 Tapas Kundu <tkundu@vmware.com> 1.2.3.2-2
- Build with python3
- Mass removal python2
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.3.2-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace.
