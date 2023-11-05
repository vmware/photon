Summary:        C library implementation of the Apache Kafka protocol
Name:           librdkafka
Version:        1.5.0
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/edenhill/librdkafka
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=ccd8dd3e90c9315833610745c28e0ffa60786324c938c7cbbb2ff847d7493d1b72d97adf5e5210bbc87970047cfd7e58a85141534d227187f2f17c492bef4262
Patch0:         lz4-CVE-2021-3520.patch
%description
librdkafka is a C library implementation of the Apache Kafka protocol, providing Producer, Consumer and Admin clients.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.a' -delete

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc %{_docdir}/librdkafka/README.md
%doc %{_docdir}/librdkafka/LICENSE
%doc %{_docdir}/librdkafka/CONFIGURATION.md
%doc %{_docdir}/librdkafka/INTRODUCTION.md
%doc %{_docdir}/librdkafka/STATISTICS.md
%doc %{_docdir}/librdkafka/LICENSES.txt
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/librdkafka
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Nov 03 2023 Harinadh D <hdommaraju@vmware.com> 1.5.0-1
- Fix CVE-2021-3520
* Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 1.3.0-1
- Initial build.  First version
