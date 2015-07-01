Summary:    The Apache Portable Runtime
Name:       apr
Version:    1.5.2
Release:    2%{?dist}
License:    Apache License 2.0
URL:        https://apr.apache.org/
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    http://archive.apache.org/dist/apr/%{name}-%{version}.tar.gz
%description
The Apache Portable Runtime.

%prep
%setup -q
%build
./configure --prefix=/usr \
        --includedir=%{_includedir}/apr-%{version} \
        --with-installbuilddir=%{_libdir}/apr/build-%{version} \
        --with-devrandom=/dev/urandom \
        CC=gcc CXX=g++

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
%{_includedir}/*

%changelog
*   Wed Jul 01 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-2
-   Fix tags and paths.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-1
-   Initial build. First version
