%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        POSIX capability Library
Name:           libcap-ng
Version:        0.7.7
Release:        3%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://people.redhat.com/sgrubb/libcap-ng
Source0:        http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
%define sha1    libcap-ng=de8ea2c89cb1506a578de7cb032da34c970dd035
BuildRequires:  python2-devel
BuildRequires:  python2-libs
Requires:       python2

%description
The libcap-ng library is intended to make programming with posix capabilities much easier than the traditional libcap library. It includes utilities that can analyse all currently running applications and print out any capabilities and whether or not it has an open ended bounding set. An open bounding set without the securebits "NOROOT" flag will allow full capabilities escalation for apps retaining uid 0 simply by calling execve.

%package  -n    python2-libcap-ng
Summary:        Python bindings for libcap-ng
License:        LGPLv2+
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  swig
Requires:       %{name} = %{version}-%{release}
Requires:       python2
%description -n python2-libcap-ng
The python2-libcap-ng package contains the python2 bindings for libcap-ng.

%package  -n    python3-libcap-ng
Summary:        Python3 bindings for libaudit
License:        LGPLv2+
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  swig
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-libcap-ng
The python3-libcap-ng package contains the python3 bindings for libcap-ng.

%package        devel
Summary:        The libraries and header files needed for libcap-ng development.
Requires:       %{name} = %{version}-%{release}

%description devel
The libraries and header files needed for libcap_ng development.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --with-python \
    --with-python3

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install 
find %{buildroot} -name '*.la' -delete

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man8/*

%files -n python2-libcap-ng
%{python2_sitelib}/*

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
*   Fri Jun 02 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.7-3
-   Move python2 requires to python subpackage and added python3.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.7-2
-   GA - Bump release of all rpms
*   Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 0.7.7-1
-   Initial version

