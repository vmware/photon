Summary:    The Apache Portable Runtime
Name:       apr
Version:    1.5.2
Release:    1%{?dist}
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
/usr/lib/*
/usr/bin/*
/usr/include/*

%changelog
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-1
-   Initial build. First version
