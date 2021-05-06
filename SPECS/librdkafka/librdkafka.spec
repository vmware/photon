Summary:        C library implementation of the Apache Kafka protocol
Name:           librdkafka
Version:        1.6.1
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/edenhill/librdkafka
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}=ed93d236670e1ec1fa47d6fa8c2b3806b0d93930

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
%doc %{_docdir}/librdkafka/CHANGELOG.md
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
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.0-1
-   Automatic Version Bump
*   Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 1.3.0-1
-   Initial build.  First version
