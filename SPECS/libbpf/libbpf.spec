Summary:        Libbpf library
Name:           libbpf
Version:        0.1.1
Release:        1%{?dist}
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPL-2.1 OR BSD-2-Clause
URL:            https://github.com/libbpf/libbpf
Source:         libbpf-%{version}.tar.gz
%define sha1    libbpf=ec8115a190fb3bc53a0f81d0b67228de166b7c45
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
%make_build -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir}

%install
%make_install -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir}

%clean
rm -rf %{buildroot}

%files
%ifarch aarch64
%attr(0755,-,-) %{_libdir}/libbpf.so.0.1.0
%{_libdir}/libbpf.so.0
%{_libdir}/libbpf.so
%endif
%ifarch x86_64
%attr(0755,-,-) %{_lib64dir}/libbpf.so.0.1.0
%{_lib64dir}/libbpf.so.0
%{_lib64dir}/libbpf.so
%endif

%files devel
%attr(0644,-,-) /usr/include/bpf/*
%ifarch aarch64
%attr(0644,-,-) %{_libdir}/libbpf.a
%attr(0644,-,-) %{_libdir}/pkgconfig/libbpf.pc
%endif
%ifarch x86_64
%attr(0644,-,-) %{_lib64dir}/libbpf.a
%attr(0644,-,-) %{_lib64dir}/pkgconfig/libbpf.pc
%endif

%changelog
* Wed Nov 11 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.1.1-1
- Initial release
