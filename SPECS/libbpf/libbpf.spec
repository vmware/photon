Summary:        Libbpf library
Name:           libbpf
Version:        0.6.1
Release:        2%{?dist}
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPL-2.1 OR BSD-2-Clause
URL:            https://github.com/libbpf/libbpf

Source0:        libbpf-%{version}.tar.gz
%define sha1 %{name}=ae84df3705c3d20464e4d257c2182680e4eb0afa

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
%autosetup -p1

%build
%make_build -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir} LIBDIR=%{_libdir} %{?_smp_mflags}

%install
%make_install -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir} LIBDIR=%{_libdir} %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%attr(0755,-,-) %{_libdir}/libbpf.so.*
%{_libdir}/libbpf.so.0
%{_libdir}/libbpf.so

%files devel
%attr(0644,-,-) %{_includedir}/bpf/*
%attr(0644,-,-) %{_libdir}/libbpf.a
%attr(0644,-,-) %{_libdir}/pkgconfig/libbpf.pc

%changelog
* Thu Mar 17 2022 Shreenidhi Shedi <msikka@vmware.com> 0.6.1-2
- Fix aarch64 build
* Wed Jan 12 2022 Susant Sahani <ssahani@vmware.com>  0.6.1-1
- Version Bump
* Fri Oct 16 2020 Michelle Wang <michellew@vmware.com> 0.1.1-2
- Fix build error in aarch64 platform
* Mon Oct 05 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.1.0-1
- Initial release
