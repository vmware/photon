Summary:        Tool to manage UEFI Secure Boot MoK Keys
Name:           mokutil
Version:        0.7.1
Release:        1%{?dist}
URL:            https://github.com/lcp/mokutil
License:        GPLv3
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/lcp/mokutil/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512  %{name}=2689207dbc8cbe17d4db25848acbea93403ac5ef20735f277de80cac3b8673c4ad9b42b2d7cf6190556cea185cbd5a5a4d812ae7657c20959c5d4d9101ac300d
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
* Wed Feb 14 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 0.7.1-1
- Package version upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.6.0-2
- Bump version as a part of openssl upgrade
* Fri Sep 29 2023 Kuntal Nayak <nkuntal@vmware.com> 0.6.0-1
- Initial independent package
