Name:           gnu-efi
Version:        3.0.14
Release:        1%{?dist}
Summary:        Development Libraries and headers for EFI
License:        BSD
URL:            https://sourceforge.net/projects/gnu-efi
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://download.sourceforge.net/gnu-efi/%{name}-%{version}.tar.bz2
%define sha1 %{name}=e46b3726478838e85d0a79d0a0d3508c4f2995cf

BuildRequires: binutils
BuildRequires: gcc
BuildRequires: make

%define debug_package %{nil}

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%autosetup -p1 -n gnu-efi-%{version}

%build
export CFLAGS+=" -ffat-lto-objects"
%make_build %{?_smp_mflags}
%make_build -C lib %{?_smp_mflags}
%make_build -C gnuefi %{?_smp_mflags}
%make_build -C inc %{?_smp_mflags}
export LDFLAGS=""
%make_build -C apps %{?_smp_mflags}

%install
%make_install %{?_smp_mflags} PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot}

%files
%{_includedir}/efi
%{_libdir}/elf_%{_arch}_efi.lds
%{_libdir}/crt0-efi-%{_arch}.o
%{_libdir}/libefi.a
%{_libdir}/libgnuefi.a

%changelog
* Tue Jan 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.14-1
- Intial version needed for systemd-250.x
