Summary:        A container monitor utility
Name:           conmon
Version:        2.1.7
Release:        5%{?dist}
URL:            https://github.com/containers/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        conmon-%{version}.tar.gz
%define sha512  %{name}=95d394b399a19a62b894cdd03937ab79b81051eea1db461b1bf957ddd7626d6ca4aa108b8319ed8c08adbdf99fd960c5ba29146e8b0673b5c920708912a72973

Source1: license.txt
%include %{SOURCE1}
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
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2.1.7-5
- Release bump for SRP compliance
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.1.7-4
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.1.7-3
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 2.1.7-2
- Bump version as a part of go upgrade
* Fri Jun 30 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.1.7-1
- Upgrade to v2.1.7
* Mon Dec 19 2022 Nitesh Kumar <kunitesh@vmware.com> 2.1.5-1
- Version upgrade to v2.1.5
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 2.1.4-1
- Initial version
