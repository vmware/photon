Summary:    Logging Libraries
Name:       liblogging
Version:    1.0.6
Release:    2%{?dist}
License:    BSD
URL:        http://www.liblogging.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://download.rsyslog.com/liblogging/liblogging-%{version}.tar.gz
%define sha512 %{name}=09c90a93b2d32afa44be5a800705a64690810a56d21bed1455cb70680b01fecd4efef3881a43f98ebcafa996b6046ed8e5af935eacc12014f330a7fd23674964

%description
liblogging (the upstream project) is a collection of several components.
Namely: stdlog, journalemu, rfc3195.
The stdlog component of liblogging can be viewed as an enhanced version of the
syslog(3) API. It retains the easy semantics, but makes the API more
sophisticated "behind the scenes" with better support for multiple threads
and flexibility for different log destinations (e.g. syslog and systemd
journal).

%package devel
Summary:    Development libraries and header files for liblogging
Requires:   liblogging

%description devel
The package contains libraries and header files for
developing applications that use liblogging.

%prep
%autosetup -p1

%build
%configure --disable-journal
%make_build

%install
%make_install

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/liblogging/*.h

%changelog
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.6-2
- Remove .la files
* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.6-1
- Updated to version 1.0.6
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.5-2
- GA - Bump release of all rpms
* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.5-1
- Initial build. First version
