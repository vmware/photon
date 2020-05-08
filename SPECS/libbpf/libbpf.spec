Summary:        Libbpf library
Name:           libbpf
Version:        0.1.0
Release:        1%{?dist}
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon

License:        GPL-2.1 OR BSD-2-Clause
URL:            https://github.com/libbpf/libbpf
Source:         libbpf-%{version}.tar.gz
%define sha1    libbpf=cd1b5690a1d1c00cddce7118b02355fc1c634a2a

BuildRequires:  elfutils-libelf-devel
BuildRequires:  elfutils-devel

Requires:  elfutils-libelf
Requires:  elfutils

%description
Library for loading eBPF programs and reading and manipulating eBPF objects from user-space

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The libbpf-devel package contains libraries header files for
developing applications that use libbpf.

%prep
%autosetup

%build
%make_build -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir}

%install
%make_install -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir}

%clean
rm -rf %{buildroot}

%files
%attr(0755,-,-) %{_lib64dir}/libbpf.so.%{version}
%{_lib64dir}/libbpf.so.0
%{_lib64dir}/libbpf.so

%files devel
%attr(0644,-,-) /usr/include/bpf/*
%attr(0644,-,-) %{_lib64dir}/libbpf.a
%attr(0644,-,-) %{_lib64dir}/pkgconfig/libbpf.pc

%changelog
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.1.0-1
- Initial release
