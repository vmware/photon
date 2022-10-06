Summary:        Bash Automated Testing System
Name:           bats
Version:        1.8.0
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Tool
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://github.com/bats-core/bats-core
SOURCE0:        https://github.com/bats-core/bats-core/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=e51ea85bf2f455881a90220d783b4a261bd91331326a7184eb31ea9adf31c18a79a062fd77af12d082ccef953d992382ec19ca9a27395b2a03c4a9a120bdda76

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
* Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.8.0-1
- Automatic Version Bump
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 1.7.0-1
- Initial version, Needed by podman-tests
