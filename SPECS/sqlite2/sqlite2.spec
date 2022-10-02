Summary:        SQLite: An Embeddable SQL Database Engine
Name:           sqlite2
Version:        2.8.17
Release:        4%{?dist}
URL:            http://www.sqlite.org
License:        Public Domain
Group:          System Environment/GeneralLibraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.sqlite.org/sqlite-%{version}.tar.gz
%define sha512 sqlite=966e0b7f7ebbaaa9e1899864475040946fd7b66363be778d29fadd5184623b1e62644f3c8d4c4ecd001b88044befa7c34d9de9f68590329a1a8301d854b73e3f

Patch0:         0001-lemon-fix.patch

%description
SQLite is a self-contained, high-reliability, embedded, full-featured, public-domain, SQL database engine. SQLite is the most used database engine in the world.

%package devel
Summary: Headers and development libraries for sqlite2
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Headers and development libraries for sqlite2

%prep
%autosetup -p1 -n sqlite-%{version}

%build
%configure \
       --enable-threads \
       --enable-shared \
       --enable-symbols

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libsqlite.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libsqlite.a
%{_libdir}/libsqlite.so

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.8.17-4
- Remove .la files
* Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 2.8.17-3
- adding patch to fix lemon segmentation fault
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.8.17-2
- Use standard configure macros
* Wed Apr 12 2017 Xiaolin Li <xiaolinl@vmware.com>  2.8.17-1
- Initial build.  First version
