Summary:        Bash Automated Testing System
Name:           bats
Version:        1.7.0
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Tool
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://github.com/bats-core/bats-core
SOURCE0:        https://github.com/bats-core/bats-core/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=22ca033e004087cabf645417ea184d2e1a0704575f702a94de5b63b3af6d1fd4caaecad86a5cb49687c606728d875dd13b4d5de66599b83324980fdc71cb92e2

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
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 1.7.0-1
- Initial version, Needed by podman-tests
