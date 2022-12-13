Summary:        A container monitor utility
Name:           conmon
Version:        2.1.5
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/containers/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        conmon-%{version}.tar.gz
%define sha512  %{name}=84d3cd512e3536281789cf4b592b9799d1302d246f67712287f768eaaad93e25de52e9773dd91e3327f464bd4a294214905c681860a7c7b9e28441247a5e0814
Group:          Tools/Podman
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  go-md2man
BuildRequires:  git
BuildRequires:  glib-devel
BuildRequires:  libseccomp-devel
BuildRequires:  systemd-devel

Requires:       systemd
Requires:       libseccomp

%description
%{name} is a command-line program for monitoring and managing the lifecycle of Linux
containers that follow the Open Container Initiative (OCI) format.

%prep
%autosetup -p1

%build
make %{?_smp_mflags} DEBUGFLAG="-g" bin/conmon
make %{?_smp_mflags} GOMD2MAN=go-md2man -C docs

%install
make %{?_smp_mflags} PREFIX=%{buildroot}%{_prefix} install.bin install.crio
make %{?_smp_mflags} PREFIX=%{buildroot}%{_prefix} -C docs install

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libexecdir}/crio/%{name}
%dir %{_libexecdir}/crio
%{_mandir}/man8/%{name}.8.gz

%changelog
* Mon Dec 19 2022 Nitesh Kumar <kunitesh@vmware.com> 2.1.5-1
- Version upgrade to v2.1.5
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 2.1.4-1
- Initial version
