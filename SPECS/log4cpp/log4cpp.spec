Summary:        Log for C++
Name:           log4cpp
Version:        1.1.3
Release:        3%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://log4cpp.sourceforge.net/
Source0:         ftp://download.sourceforge.net/pub/sourceforge/log4cpp/%{name}-%{version}.tar.gz
%define sha512  log4cpp=88e5e10bce8d7d6421c3dcf14aa25385159c4ae52becdc1f3666ab86e1ad3f633786d82afe398c517d4faaa57b3e7b7c0b524361d81c6b9040dbded5cecc19de
BuildArch:      x86_64

Source1: license.txt
%include %{SOURCE1}

%description
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

%package devel
Summary: development tools for Log for C++
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %name-devel package contains the static libraries and header files
needed for development with %name.

%prep
%autosetup -p1 -n log4cpp
CC=%{__cc} CXX=%{__cxx} ./configure --prefix=%{_prefix}

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_prefix/lib/lib*.so.*

%files devel
%defattr(-,root,root)
%_prefix/include/*
%_prefix/bin/log4cpp-config
%_prefix/lib/lib*.so
%_prefix/lib/*.*a
%_prefix/lib/pkgconfig/log4cpp.pc
%_prefix/share/aclocal/*.m4

%changelog
*   Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.1.3-3
-   Release bump for SRP compliance
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.1.3-2
-   Adding BuildArch
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.1.3-1
-   Upgrade to latest version
*   Mon Oct 23 2017 Benson Kwok <bkwok@vmware.com> 1.1.1-1
-   Initial build. First version
