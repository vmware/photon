Summary:	ALSA library
Name:		alsa-lib
Version:	1.1.7
Release:	1
License:	LGPLv2+
URL:		http://alsa-project.org
Group:		Applications/Internet
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.1.7.tar.bz2
%define sha1 alsa-lib=eca62790517220297ec82ba8a5258bcb6e708866
BuildRequires:	python2-devel python2-libs
Requires:	python2
%description
The ALSA Library package contains the ALSA library used by programs
(including ALSA Utilities) requiring access to the ALSA sound interface.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
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
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace
