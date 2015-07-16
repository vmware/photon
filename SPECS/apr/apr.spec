Summary:    The Apache Portable Runtime
Name:       apr
Version:    1.5.2
Release:    4%{?dist}
License:    Apache License 2.0
URL:        https://apr.apache.org/
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    http://archive.apache.org/dist/apr/%{name}-%{version}.tar.gz
%define sha1 apr=2ef2ac9a8de7f97f15ef32cddf1ed7325163d84c
%define	    aprver  1
%description
The Apache Portable Runtime.

%prep
%setup -q
%build
./configure --prefix=/usr \
        --includedir=%{_includedir}/apr-%{aprver} \
        --with-installbuilddir=%{_libdir}/apr/build-%{aprver} \
        --with-devrandom=/dev/urandom \
        CC=gcc CXX=g++

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post

%files
%defattr(-,root,root)
%{_libdir}/*
%exclude %{_libdir}/debug
%{_bindir}/*
%{_includedir}/*

%changelog
*   Wed Jul 15 2015 Sarah Choi <sarahc@vmware.com> 1.5.2-4
-   Use aprver(=1) instead of version for mesos
*   Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.2-3
-   Exclude /usr/lib/debug
*   Wed Jul 01 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-2
-   Fix tags and paths.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-1
-   Initial build. First version
