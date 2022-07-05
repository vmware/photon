Summary:	Library for manipulating pipelines
Name:		libpipeline
Version:	1.5.5
Release:	1%{?dist}
License:	GPLv3+
URL:		http://libpipeline.nongnu.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://download.savannah.gnu.org/releases/libpipeline/%{name}-%{version}.tar.gz
%define sha512  libpipeline=adb228325c1f11e9f3566f2fc63541a90c88fe24656fc74ed0294d1eb3b80073bf4741fe7c289f53b340702145b11637d37682e3036dce41ec0fe45dcc6d62c5

%if %{with_check}
BuildRequires:  check
BuildRequires:  pkg-config
%endif

%description
Contains a library for manipulating pipelines of sub processes
in a flexible and convenient way.

%package        devel
Summary:        Library providing headers and static libraries to libpipeline
Group:          Development/Libraries
Requires:       libpipeline = %{version}-%{release}
Provides:       pkgconfig(libpipeline)

%description    devel
Development files for libpipeline

%prep
%autosetup
%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
#find %{buildroot}/%{_libdir} -name '*.la' -delete

%check
make -C tests check %{?_smp_mflags}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.5.5-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.3-1
- Automatic Version Bump
* Tue Jul 07 2020 Shreenidhi Shedi <photon-checkins@vmware.com> 1.5.2-1
- Upgrade version to 1.5.2
* Mon Aug 19 2019 Shreenidhi Shedi <sshedi@vmware.com> 1.5.0-2
- Fix make check
* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.5.0-1
- Update to 1.5.0
- Split development files to devel package
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.1-2
- GA - Bump release of all rpms
* Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.1-1
- Initial build. First version
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.6-1
- Initial build. First version
