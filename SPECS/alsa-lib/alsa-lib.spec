Summary:        ALSA library
Name:           alsa-lib
Version:        1.2.3.2
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://alsa-project.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}.tar.bz2
%define sha1    alsa-lib=2dfe24ae4872c0a390791a515d50de4047eff02b
BuildRequires:	python3-devel python3-libs
Requires:       python3
%description
The ALSA Library package contains the ALSA library used by programs
(including ALSA Utilities) requiring access to the ALSA sound interface.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Mon Jul 20 2020 Tapas Kundu <tkundu@vmware.com> 1.2.3.2-2
- Build with python3
- Mass removal python2
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.3.2-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace
