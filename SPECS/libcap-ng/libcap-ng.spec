%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        POSIX capability Library
Name:           libcap-ng
Version:        0.7.11
Release:        1%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
URL:            http://people.redhat.com/sgrubb/libcap-ng
Source0:        http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
%define sha1    libcap-ng=0e0fefa86325c7c54ffd096b0aa2de5559c0984b
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  swig

%description
The libcap-ng library is intended to make programming with posix capabilities much easier than the traditional libcap library. It includes utilities that can analyse all currently running applications and print out any capabilities and whether or not it has an open ended bounding set. An open bounding set without the securebits "NOROOT" flag will allow full capabilities escalation for apps retaining uid 0 simply by calling execve.

%package  -n    python3-libcap-ng
Summary:        Python3 bindings for libaudit
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-libcap-ng
The python3-libcap-ng package contains the python3 bindings for libcap-ng.

%package devel
Summary:    The libraries and header files needed for libcap-ng development.
Requires:   %{name} = %{version}-%{release}

%description devel
The libraries and header files needed for libcap_ng development.

%prep
%setup -q

%build
%configure \
    --with-python3

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man8/*

%files -n python3-libcap-ng
%{python3_sitelib}/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_datadir}/aclocal/*.m4
%{_libdir}/*.a

%changelog
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 0.7.11-1
-   Automatic Version Bump
*   Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 0.7.10-1
-   Automatic Version Bump
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 0.7.9-3
-   Mass removal python2
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 0.7.9-2
-   Cross compilation support
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 0.7.9-1
-   Updated to latest version
*   Mon May 22 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.8-2
-   Added python3 subpackage.
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 0.7.8-1
-   Upgrade version to 0.7.8
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 0.7.7-3
-   Moved man3 to devel subpackage.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.7-2
-   GA - Bump release of all rpms
*   Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 0.7.7-1
-   Initial version

