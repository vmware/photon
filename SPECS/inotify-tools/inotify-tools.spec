Summary:        Command line utility for i-node notifications and management.
Name:           inotify-tools
Version:        3.13
Release:        2%{?dist}
URL:            http://sourceforge.net/projects/inotify-tools
License:        GPLv2+ and GPLv3+ and LGPLv2+
Group:          Applications/Systems
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sourceforge.net/projects/inotify-tools/files/latest/download/%{name}-%{version}.tar.gz
Provides:       libinotifytools0

%define sha1 inotify-tools=4f9c027e441a84e78b36f9c1a87bf1896216b5ff

%description
inotify-tools is simple command line interface program for linux distributions
which is used to monitor inode specific filesystem events.

%package devel
Summary: Header files and libraries for building application using libinotify-tools.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q


%build
%configure
make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != '/' ] && rm -rf $RPM_BUILD_ROOT
%makeinstall


%post -p /sbin/ldconfig

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != '/' ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin
/usr/share
/%{_libdir}/libinotifytools.so.0.4.1

%files devel
%defattr(-,root,root)
/usr/include
/%{_libdir}/libinotifytools.a
/%{_libdir}/libinotifytools.so
/%{_libdir}/libinotifytools.so.0
/%{_libdir}/libinotifytools.la

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.13-2
-	GA - Bump release of all rpms
*       Mon Dec 14 2015 Kumar Kaushik <kaushikk@vmware.com> 3.13-1
-       Initial build.  First version

