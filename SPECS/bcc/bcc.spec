%global debug_package %{nil}

Name:            bcc
Summary:         BPF Compiler Collection (BCC)
Version:         0.28.0
Release:         3%{?dist}
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
URL:             https://github.com/iovisor/bcc

Source0: https://github.com/iovisor/bcc/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:        CVE-2024-2314-1.patch
Patch1:        CVE-2024-2314-2.patch

BuildRequires: cmake
BuildRequires: build-essential
BuildRequires: libstdc++
BuildRequires: elfutils-libelf-devel-static
BuildRequires: elfutils-libelf-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: llvm-devel
BuildRequires: clang-devel
BuildRequires: pkg-config
BuildRequires: ncurses-devel
BuildRequires: curl-devel
BuildRequires: libbpf-devel
BuildRequires: zip

Requires: curl-libs

%description
BCC is a toolkit for creating efficient kernel tracing and manipulation programs,
and includes several useful tools and examples. It makes use of
extended BPF (Berkeley Packet Filters), formally known as eBPF,
a new feature that was first added to Linux 3.15.
Much of what BCC uses requires Linux 4.1 and above.

%package         devel
Summary:         Shared Library for BPF Compiler Collection (BCC)
Requires:        %{name} = %{version}-%{release}

%description     devel
%{name}-devel contains shared libraries and header files for
developing application.

%package -n      python3-%{name}
Summary:         Python3 bindings for BPF Compiler Collection (BCC)
Requires:        %{name} = %{version}-%{release}

%description -n  python3-%{name}
Python bindings for BPF Compiler Collection (BCC)

%package         examples
Summary:         Examples for BPF Compiler Collection (BCC)
Requires:        python3-%{name} = %{version}-%{release}

%description     examples
Examples for BPF Compiler Collection (BCC)

%package         tools
Summary:         Command line tools for BPF Compiler Collection (BCC)
Requires:        python3-%{name} = %{version}-%{release}

%description     tools
Command line tools for BPF Compiler Collection (BCC)

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%cmake -DREVISION_LAST=%{version} \
       -DREVISION=%{version} \
       -DPYTHON_CMD=%{python3} \
       -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_USE_LIBBPF_PACKAGE=TRUE

%cmake_build

%install
%cmake_install
# mangle shebangs
find %{buildroot}%{_datadir}/%{name}/{tools,examples} -type f -exec \
    sed -i -e '1 s|^#!/usr/bin/python$|#!'%{python3}'|' \
           -e '1 s|^#!/usr/bin/env python$|#!'%{python3}'|' {} \;

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE.txt
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}_bpf.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_bpf.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/%{name}/

%files -n python3-%{name}
%defattr(-,root,root)
%{python3_sitelib}/%{name}*

%files examples
%defattr(-,root,root)
%{_datadir}/%{name}/examples/*

%files tools
%defattr(-,root,root)
%{_datadir}/%{name}/introspection/*
%{_datadir}/%{name}/tools/*
%{_datadir}/%{name}/man/*

%changelog
* Mon Dec 23 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.28.0-3
- CVE-2024-2314 fix
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 0.28.0-2
- Release bump for SRP compliance
* Sun Aug 27 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.28.0-1
- Upgrade to v0.28.0
* Thu Apr 13 2023 Harinadh D <hdommaraju@vmware.com> 0.25.0-4
- Bump up to use curl 8.0.1
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.25.0-3
- Bump up due to change in elfutils
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.25.0-2
- Update release to compile with python 3.11
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.25.0-1
- Upgrade to v0.25.1
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.19.0-2
- Use cmake macros for build and install
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 0.19.0-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.16.0-1
- Automatic Version Bump
* Wed Jun 26 2019  Keerthana K <keerthanak@vmware.com> 0.10.0-1
- Initial bcc package for PhotonOS.
