Summary:        Tool to manage UEFI Secure Boot MoK Keys
Name:           mokutil
Version:        0.6.0
Release:        2%{?dist}
URL:            https://github.com/lcp/mokutil
License:        GPLv3
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/lcp/mokutil/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512  %{name}=11a9d172dba4fbb674e58e5d82cb1dc65a80cff844c0eaebd106b4d4608b24a8207e0cfabf36fe1eedb67f68a8a18db2136c7b62aa3230ac104615e8284dbd7d
BuildArch:      x86_64

BuildRequires:  which
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  openssl
BuildRequires:  efivar-devel
BuildRequires:  keyutils-devel

Requires: efivar
Requires: keyutils
Requires: openssl
Requires: glibc

%description
The utility to manipulate Machines Owner Keys that are managed in shim

%prep
%autosetup -p1

%build
./autogen.sh --prefix=%{_usr}
%make_build

%install
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/%{name}

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.6.0-2
- Bump version as a part of openssl upgrade
* Fri Sep 29 2023 Kuntal Nayak <nkuntal@vmware.com> 0.6.0-1
- Initial independent package
