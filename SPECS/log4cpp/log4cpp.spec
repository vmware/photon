Summary:        Log for C++
Name:           log4cpp
Version:        1.1.1
Release:        1%{?dist}
License:        LGPL
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://log4cpp.sourceforge.net/
Source:         ftp://download.sourceforge.net/pub/sourceforge/log4cpp/%name-%version.tar.gz
%define sha1    log4cpp=23aa5bd7d6f79992c92bad3e1c6d64a34f8fcf68

%description
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

%package devel
Summary: development tools for Log for C++
Group: Development/Libraries
Requires: %name = %version

%description devel
The %name-devel package contains the static libraries and header files
needed for development with %name.


%prep
%{__rm} -rf $RPM_BUILD_ROOT

%setup -q -n log4cpp
CC=%{__cc} CXX=%{__cxx} ./configure --prefix=%{_prefix} 

%build
%{__make}

%install
%{__rm} -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

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


