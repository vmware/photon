Name:          crun
Version:       1.8
Release:       8%{?dist}
Summary:       OCI runtime in C
Group:         Development/Other
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/containers/crun
Source0:       https://github.com/containers/crun/releases/download/%{version}/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}
BuildRequires: libcap-devel
BuildRequires: libseccomp-devel
BuildRequires: systemd-devel
BuildRequires: python3
BuildRequires: yajl-devel
BuildRequires: git
BuildRequires: libgcrypt-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: go-md2man
BuildRequires: libtool
BuildRequires: protobuf-c-devel
BuildRequires: make
BuildRequires: libselinux-devel
BuildRequires: gcc
BuildRequires: pkg-config

Requires:      glibc
Requires:      libcap
Requires:      libseccomp
Requires:      systemd

%description
A fast and low-memory footprint OCI Container Runtime fully written in C

%prep
%autosetup -Sgit -n %{name}-%{version}

%build
./autogen.sh

%configure \
        --disable-silent-rules \
        --enable-embedded-yajl=yes
%make_build

%install
%make_install
rm -f %{buildroot}%{_prefix}/lib/*.la \
      %{buildroot}%{_prefix}/lib/*.a

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/%{name}
%{_mandir}/*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.8-8
- Release bump for SRP compliance
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.8-7
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.8-6
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.8-5
- Bump version as a part of go upgrade
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.8-4
- Bump version as a part of protobuf upgrade
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.8-3
- Bump version as a part of protobuf upgrade
* Tue Jun 06 2023 Mukul Sikka <msikka@vmware.com> 1.8-2
- Bump up release for protobuf-c
* Fri Feb 10 2023 Gerrit Photon <photon-checkins@vmware.com> 1.8-1
- Automatic Version Bump
* Wed Jun 08 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.4.5-1
- crun initial build
