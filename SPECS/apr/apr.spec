Summary:        The Apache Portable Runtime
Name:           apr
Version:        1.6.5
Release:        1%{?dist}
License:        Apache License 2.0
URL:            https://apr.apache.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.gz
%define sha1    %{name}=ebf4f15fa5003b1490550e260f5a57dc8a2ff0ac
%define         aprver  1
%description
The Apache Portable Runtime.
%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications 

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

%check
make %{?_smp_mflags} check

%post

%files
%defattr(-,root,root)
%{_libdir}/*
%exclude %{_libdir}/debug
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%{_bindir}/*

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
*   Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 1.6.5-1
-   Updated to version 1.6.5
*   Fri Dec 08 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.2-7
-   Fix CVE-2017-12613
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.2-6
-   GA - Bump release of all rpms
*   Mon Sep 21 2015 Harish Udaiya Kumar<hudaiyakumar@vmware.com> 1.5.2-5
-   Repacked to move the include files in devel package.
*   Wed Jul 15 2015 Sarah Choi <sarahc@vmware.com> 1.5.2-4
-   Use aprver(=1) instead of version for mesos
*   Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.2-3
-   Exclude /usr/lib/debug
*   Wed Jul 01 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-2
-   Fix tags and paths.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-1
-   Initial build. First version
