Summary:    Provides IPC between GnuPG Components
Name:       libassuan
Version:    2.5.3
Release:    2%{?dist}
License:    GPLv3+
URL:        https://www.gnupg.org/(fr)/related_software/libassuan/index.html
Group:      Development/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://www.gnupg.org/ftp/gcrypt/libassuan/%{name}-%{version}.tar.bz2
%define sha512 %{name}=e7ccb651ea75b07b2e687d48d86d0ab83cba8e2af7f30da2aec794808e13e6ec93f21d607db50d3431f1c23cb3a07a2793b71170e69fa2f5a82cffb81961f617

BuildRequires:  libgpg-error-devel >= 1.21

Requires:   libgpg-error >= 1.21

%description
The %{name} package contains an inter process communication library
used by some of the other GnuPG related packages. %{name}'s primary use
is to allow a client to interact with a non-persistent server.
%{name} is not, however, limited to use with GnuPG servers and clients.
It was designed to be flexible enough to meet the demands
of many transaction based environments with non-persistent servers.

%package devel
Summary: GnuPG IPC library
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
This is the IPC static library used by GnuPG 2, GPGME and a few other
packages.

This package contains files needed to develop applications using %{name}.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

rm -rf %{buildroot}%{_libdir}/*.la \
       %{buildroot}%{_infodir}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/%{name}-config

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/%{name}.m4

%changelog
* Tue May 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.5.3-2
- Fix packaging, add devel sub package
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.3-1
- Automatic Version Bump
* Fri Sep 21 2018 Keerthana K <keerthanak@vmware.com> 2.5.1-1
- Update to version 2.5.1
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.3-1
- Upgrade version to 2.4.3
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.4.2-3
- BuildRequired libgpg-error-devel.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.2-2
- GA - Bump release of all rpms
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.2-1
- Updated to version 2.4.2
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.2.0-2
- Updated group.
* Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> 2.2.0-1
- Initial version
