Summary:        NUMA support for Linux
Name:           numactl
Version:        2.0.13
Release:        3%{?dist}
License:        GPLv2
URL:            https://github.com/numactl/numactl
Source0:        https://github.com/numactl/numactl/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=f7b747eb8f3ded9f3661cb0fc7b65b5ed490677f881f8fe6a000baf714747515853b4e5c8781b014241180bf16e9f0bfdf2c6f758725e34b4938696ba496b72a
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
%description
Simple NUMA policy support. It consists of a numactl program to run other programs with a specific NUMA policy.

%package -n libnuma
License:        LGPLv2.1
Summary:        Development libraries and header files for jsoncpp
Requires:       %{name} = %{version}-%{release}
%description -n libnuma
libnuma shared library ("NUMA API") to set NUMA policy in applications.

%package -n libnuma-devel
Summary:        Development libraries and header files for jsoncpp
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
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

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
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.13-3
- Remove .la files
* Tue Sep 29 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0.13-2
- Fix libnuma-devel dependency
* Mon Nov 18 2019 Alexey Makhalov <amakhalov@vmware.com> 2.0.13-1
- Initial build. First version
