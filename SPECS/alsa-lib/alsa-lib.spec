Summary:        ALSA library
Name:           alsa-lib
Version:        1.2.6.1
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://alsa-project.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.alsa-project.org/files/pub/lib/%{name}-%{version}.tar.bz2
%define sha512  %{name}=70e539cf092b5d43e00e4134d8a3e184f0dc34312823e4b58a574320cbf06cb7369bc3251ecb1858033756a7a8c35d36faa8da48d49f6efe0cec905784adbd45

BuildRequires:  python3-devel

Requires:       python3

%description
The ALSA Library package contains the ALSA library used by programs
(including ALSA Utilities) requiring access to the ALSA sound interface.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
rm -f %{buildroot}%{_libdir}/*.la

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%exclude %dir %{_libdir}/debug
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
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
