Summary:        Libbpf library
Name:           libbpf
Version:        0.6.1
Release:        2%{?dist}
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPL-2.1 OR BSD-2-Clause
URL:            https://github.com/libbpf/libbpf
Source:         libbpf-%{version}.tar.gz
%define sha1    libbpf=ae84df3705c3d20464e4d257c2182680e4eb0afa

BuildRequires:  elfutils-libelf-devel
BuildRequires:  elfutils-devel

Requires:       elfutils-libelf
Requires:       elfutils

%description
Library for loading eBPF programs and reading and manipulating eBPF objects from user-space

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The libbpf-devel package contains libraries header files for
developing applications that use libbpf.

%prep
%autosetup

%build
%make_build -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir} LIBDIR=%{_libdir}

%install
%make_install -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir} LIBDIR=%{_libdir}

%clean
rm -rf %{buildroot}

%files
%attr(0755,-,-) %{_libdir}/libbpf.so.0.6.0
%{_libdir}/libbpf.so.0
%{_libdir}/libbpf.so

%files devel
%attr(0644,-,-) /usr/include/bpf/*
%attr(0644,-,-) %{_libdir}/libbpf.a
%attr(0644,-,-) %{_libdir}/pkgconfig/libbpf.pc

%changelog
* Mon Feb 21 2022 Mukul Sikka <msikka@vmware.com>  0.6.1-2
- Fix build error in aarch64 platform
* Wed Jan 12 2022 Susant Sahani <ssahani@vmware.com>  0.6.1-1
- Version Bump
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 0.3-1
- Automatic Version Bump
* Fri Oct 16 2020 Michelle Wang <michellew@vmware.com> 0.1.1-2
- Fix build error in aarch64 platform
* Mon Oct 05 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.1.0-1
- Initial release
