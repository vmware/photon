Summary:    slirp for network namespaces
Name:       slirp4netns
Version:    1.2.0
Release:    1%{?dist}
License:    GPLv2
URL:        https://github.com/rootless-containers/%{name}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:    %{url}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=4ede7323aab92d0ad0026bc5e1aefc07898a5b50c4ff57c13eb9d8e75d73a4bb5ac992f021404053fcba2b05c56dcafcbfefbc4bbc47f72a0797ab62bd76a60a

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
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- Introduce slirp4netns. Needed for rootlesskit
