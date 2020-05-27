Summary:    C library implementation of the Apache Kafka protocol
Name:       librdkafka
Version:    1.3.0
Release:    1%{?dist}
License:    BSD
URL:        https://github.com/edenhill/librdkafka
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    %{name}-%{version}.tar.gz
%define sha1 %{name}=20c4ddb2437fc875ba92777a3906fb3a375d7e7f

%description
librdkafka is a C library implementation of the Apache Kafka protocol, providing Producer, Consumer and Admin clients.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files

%prep
%setup -q -n %{name}-%{version}

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.a' -delete

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md CONFIGURATION.md LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/librdkafka
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 1.3.0-1
-   Initial build.  First version
