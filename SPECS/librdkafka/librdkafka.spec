Summary:        C library implementation of the Apache Kafka protocol
Name:           librdkafka
Version:        1.8.2
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/edenhill/librdkafka
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=8c8ae291129b78e3b8367307ad1b1715af1438cd76d7160d64d13a58adf84c7c9f51efeba4656f55e101c25e4cb744db0d8bb5c01a2decb229e4567d16bdcb22
Patch0:         0001-compatibility-with-openssl-3.0.0.patch

%description
librdkafka is a C library implementation of the Apache Kafka protocol, providing Producer, Consumer and Admin clients.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}

%description	devel
It contains the libraries and header files

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install %{?_smp_mflags}
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
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.8.2-1
-   Automatic Version Bump
*   Fri Jun 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.6.1-2
-   openssl 3.0.0 compatibility
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.0-1
-   Automatic Version Bump
*   Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 1.3.0-1
-   Initial build.  First version.
