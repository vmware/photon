Summary:        Bash Automated Testing System
Name:           bats
Version:        1.8.2
Release:        2%{?dist}
Group:          System Environment/Tool
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://github.com/bats-core/bats-core
Source0:        https://github.com/bats-core/bats-core/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=7eace32f19789e081112af1ce8ab33ff210d52bd3ea84962bbec226349b3b8d8912b6a495f5524f9cc7cfe692f1d23d684c93c24e182752e2b30731670d6eeea

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  parallel
BuildRequires:  procps-ng

Requires:       bash
Requires:       parallel

%description
Bats is a TAP-compliant testing framework for Bash. It provides a simple way to
verify that the UNIX programs you write behave as expected. Bats is most useful
when testing software written in Bash, but you can use it to test any UNIX
program.

%prep
%autosetup -n bats-core-%{version}

%install
./install.sh %{buildroot}%{_prefix}

%check
./bin/bats test

%files
%defattr(-,root,root)
%doc AUTHORS README.md docs/CHANGELOG.md
%license LICENSE.md
%{_bindir}/%{name}
%{_libexecdir}/%{name}-core
%{_prefix}/lib/%{name}-core
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man7/%{name}.7.gz

%changelog
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.8.2-2
- Release bump for SRP compliance
* Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 1.8.2-1
- Automatic Version Bump
* Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.8.0-1
- Automatic Version Bump
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 1.7.0-1
- Initial version, Needed by podman-tests
