Summary:    slirp for network namespaces
Name:       slirp4netns
Version:    1.2.0
Release:    6%{?dist}
URL:        https://github.com/rootless-containers/%{name}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:    %{url}/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: glib-devel
BuildRequires: go-md2man
BuildRequires: libcap-devel
BuildRequires: libseccomp-devel
BuildRequires: libseccomp
BuildRequires: libslirp-devel
BuildRequires: make

Requires: libslirp
Requires: libseccomp

%description
slirp for network namespaces, without copying buffers across the namespaces.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure

make generate-man %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install install-man %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.2.0-6
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.0-5
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.0-4
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.2.0-3
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.2.0-2
- Bump version as a part of go upgrade
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- Introduce slirp4netns. Needed for rootlesskit
