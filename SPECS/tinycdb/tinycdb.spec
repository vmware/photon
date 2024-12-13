Name:       tinycdb
Summary:    Utility and library for manipulating constant databases
Version:    0.78
Release:    2%{?dist}
URL:        http://www.corpit.ru/mjt/tinycdb.html
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://www.corpit.ru/mjt/%{name}/%{name}-%{version}.tar.gz
%define sha512 %{name}=8930086b8e7fddcd4dbd3354c5f5ee05171df68fde1cc222b6c402430042b6e761efbad7e5fa8de18e1d36390f1526cc3e605c5086fe1c363ba1df6c03201553
Source1:    libcdb.pc

Source2: license.txt
%include %{SOURCE2}

BuildRequires: make
BuildRequires: gcc

%description
tinycdb is a small, fast and reliable utility and subroutine library for
creating and reading constant databases. The database structure is tuned
for fast reading.

This package contains tinycdb utility and shared library.

%package devel
Summary:    Development files for tinycdb
Requires:   %{name} = %{version}-%{release}

%description devel
tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases.

This package contains tinycdb development library and header file for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
make %{?_smp_mflags} staticlib sharedlib cdb-shared CFLAGS="%{optflags}"

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig

make DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir} \
    install install-sharedlib INSTALLPROG=cdb-shared CP="cp -p" %{?_smp_mflags}

chmod +x %{buildroot}%{_libdir}/*.so.*
rm -f %{buildroot}%{_libdir}/lib*.a
cp %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc NEWS ChangeLog
%{_bindir}/cdb
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_mandir}/man3/*.3*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Dec 13 2024 Dweep Advani <dweep.advani@broadcom.com> 0.78-2
- Release bump for SRP compliance
* Wed Feb 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.78-1
- Initial version. Needed for sendmail-8.17.1
