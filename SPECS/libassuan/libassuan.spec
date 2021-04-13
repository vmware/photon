Summary:	Provides IPC between GnuPG Components
Name:		libassuan
Version:	2.5.5
Release:	1%{?dist}
License:	GPLv3+
URL:		https://www.gnupg.org/(fr)/related_software/libassuan/index.html
Group:		Development/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha1 libassuan=ec4f67c0117ccd17007c748a392ded96dc1b1ae9
Requires:	libgpg-error >= 1.21
BuildRequires:	libgpg-error-devel >= 1.21
%description
The libassuan package contains an inter process communication library
used by some of the other GnuPG related packages. libassuan's primary use
is to allow a client to interact with a non-persistent server.
libassuan is not, however, limited to use with GnuPG servers and clients.
It was designed to be flexible enough to meet the demands
of many transaction based environments with non-persistent servers.
%prep
%setup -q
%build
%configure
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_infodir}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*.h
%{_libdir}/*.so*
%{_libdir}/pkgconfig/libassuan.pc
%{_datadir}/aclocal/*
%changelog
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.5.5-1
-   Automatic Version Bump
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.3-1
-   Automatic Version Bump
*   Fri Sep 21 2018 Keerthana K <keerthanak@vmware.com> 2.5.1-1
-   Update to version 2.5.1
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.3-1
-   Upgrade version to 2.4.3
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.4.2-3
-   BuildRequired libgpg-error-devel.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.2-2
-   GA - Bump release of all rpms
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.2-1
-   Updated to version 2.4.2
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.2.0-2
-   Updated group.
*   Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> 2.2.0-1
-   Initial version
