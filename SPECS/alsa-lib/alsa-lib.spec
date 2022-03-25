Summary:        ALSA library
Name:           alsa-lib
Version:        1.1.9
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://alsa-project.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}.tar.bz2
%define sha1    %{name}=2404e1c377428908c5188076d5652a2a1ecd028e

BuildRequires:  python2-devel
BuildRequires:  python2-libs

Requires:       python2

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
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -fv %{buildroot}%{_libdir}/*.la

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libasound*.so*
%{_libdir}/pkgconfig/*
%{_datadir}/*
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.9-2
- Exclude debug symbols properly
* Tue Dec 15 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.9-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace
