Summary:        NUMA support for Linux
Name:           numactl
Version:        2.0.14
Release:        2%{?dist}
License:        GPLv2
URL:            https://github.com/numactl/numactl
Source0:        https://github.com/numactl/numactl/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha1    %{name}=1325d20027bbfc9ec5b840a599f6773d38b54a00
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
%description
Simple NUMA policy support. It consists of a numactl program to run other programs with a specific NUMA policy.

%package -n libnuma
License:        LGPLv2.1
Summary:        Development libraries and header files for numactl
Requires:       %{name} = %{version}-%{release}
%description -n libnuma
libnuma shared library ("NUMA API") to set NUMA policy in applications.

%package -n libnuma-devel
Summary:        Development libraries and header files for libnuma
Requires:       libnuma
Requires:       %{name} = %{version}-%{release}
%description -n libnuma-devel
The package contains libraries and header files for
developing applications that use libnuma.

%prep
%setup -q

%build
autoreconf -fiv
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%post -n libnuma  -p /sbin/ldconfig
%postun -n libnuma -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man8/*

%files -n libnuma
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n libnuma-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/numa.pc
%{_mandir}/man2/*
%{_mandir}/man3/*

%changelog
* Thu Oct 29 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0.14-2
- Fix libnuma-devel dependency
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.14-1
- Automatic Version Bump
* Mon Nov 18 2019 Alexey Makhalov <amakhalov@vmware.com> 2.0.13-1
- Initial build. First version

