Summary:        Extremely fast compression.
Name:           lz4
Version:        1.7.5
Release:        1%{?dist}
License:        BSD
URL:            http://lz4.github.io/lz4/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/lz4/lz4/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha1    lz4=a710a7d45beb0951806d2b98f0c1739107e97c14

%description
LZ4 is lossless compression algorithm, providing compression speed at 400 MB/s per core, scalable with multi-cores CPU. 
It features an extremely fast decoder, with speed in multiple GB/s per core, typically reaching RAM speed limits on multi-core systems.

%package devel
Summary:    Libraries and header files for lz4
Requires:   %{name} = %{version}-%{release}
%description devel
Static libraries and header files for the support library for lz4.

%prep
%setup -q

%build
make all

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblz4.so.*
%{_datadir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/liblz4.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*


%changelog
*   Wed Mar 29 2017 Michelle Wang <michellew@vmware.com> 1.7.5-1
-   Update lz4 package to 1.7.5.
*   Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
-   Add lz4 package.


