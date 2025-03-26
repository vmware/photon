%define guile_major_ver 2.2

Summary:        GNU Ubiquitous Intelligent Language for Extensions
Name:           guile
Version:        2.2.7
Release:        7%{?dist}
URL:            http://www.gnu.org/software/guile
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/gnu/guile/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libltdl-devel
BuildRequires:  libunistring-devel
BuildRequires:  gc-devel
BuildRequires:  libffi-devel

Requires:       libltdl
Requires:       libunistring
Requires:       gc
Requires:       libffi
Requires:       gmp
Requires:       glibc-iconv

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

%package        devel
Summary:        Development libraries and header files for guile
Requires:       %{name} = %{version}-%{release}
Requires:       libltdl-devel
Requires:       libunistring-devel
Requires:       gc-devel

%description    devel
The package contains libraries and header files for
developing applications that use guile.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --disable-error-on-warning

%make_build

%install
%make_install %{?_smp_mflags}

rm -f %{buildroot}%{_libdir}/*.scm \
      %{buildroot}%{_infodir}/* \
      %{buildroot}%{_libdir}/*.la

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/%{name}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_datadir}/aclocal/*.m4
%{_includedir}/%{name}/%{guile_major_ver}/*.h
%{_includedir}/%{name}/%{guile_major_ver}/libguile/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{name}/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.2.7-7
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.2.7-6
- Release bump for SRP compliance
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.7-5
- Bump version as a part of readline upgrade
* Sat Oct 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.7-4
- Bump version as a part of gc upgrade
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.7-3
- Remove .la files
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.7-2
- Bump version as a part of libffi upgrade
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 2.2.7-1
- Automatic Version Bump
* Thu Jul 16 2020 Tapas Kundu <tkundu@vmware.com> 2.0.13-3
- Bump to build with latest libffi
* Wed May 03 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.0.13-2
- Adding glibc-iconv to Requires section
* Wed Jan 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.0.13-1
- Bumped to latest version 2.0.13 to handle CVE-2016-8606
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.0.11-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.11-2
- GA - Bump release of all rpms
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.11-1
- Initial build. First version
