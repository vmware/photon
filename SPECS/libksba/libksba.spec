Summary:	Library for accessing X.509 and CMS data structure.
Name:		libksba
Version:	1.5.1
Release:	1%{?dist}
License:	GPLv3+
URL:		https://www.gnupg.org/(fr)/download/index.html#libksba
Group:		Security/Libraries.
Source0:        https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha1 libksba=740ac2551b33110e879aff100c6a6749284daf97
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  libgpg-error-devel >= 1.2

%description
Libksba is a library to make the tasks of working with X.509 certificates,
CMS data and related objects more easy. It provides a highlevel interface
to the implemented protocols and presents the data in a consistent way.

%prep
%setup -q

%build
%configure --disable-static \
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/ksba-config
%{_libdir}/*.so*
%{_libdir}/pkgconfig/ksba.pc
%{_includedir}/*
%{_datadir}/aclocal/ksba.m4
%{_datadir}/info/ksba.info.gz
%exclude %{_datadir}/info/dir

%changelog
*Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.5.1-1
-Automatic Version Bump
*Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
-Automatic Version Bump
*	Tue	Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.3.5-1
-	Udpated to version 1.3.5
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
-   BuildRequired libgpg-error-devel.
*   Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 1.3.4-1
-   Initial Build.
