Summary:        NUMA support for Linux
Name:           numactl
Version:        2.0.16
Release:        1%{?dist}
License:        GPLv2
URL:            https://github.com/numactl/numactl
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/numactl/numactl/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=de89bd9f4a9be0e27b21d096aa17a554c209414b5d08b6a2dbd03f8f4830fe4fc5adc88fa8cb08ae1cf75884835dacbde5b6f5d31386244a2582924d2260fcb6

%if 0%{?with_check}
Patch0: 0001-numactl-fix-physcpubind-for-single-cpu.patch
%endif

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
%autosetup -p1

%build
autoreconf -fiv
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

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
%{_libdir}/pkgconfig/numa.pc
%{_mandir}/man2/*
%{_mandir}/man3/*

%changelog
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.16-1
- Automatic Version Bump
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.14-3
- Remove .la files
* Thu Oct 29 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0.14-2
- Fix libnuma-devel dependency
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.14-1
- Automatic Version Bump
* Mon Nov 18 2019 Alexey Makhalov <amakhalov@vmware.com> 2.0.13-1
- Initial build. First version
