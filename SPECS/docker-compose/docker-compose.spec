%global debug_package %{nil}

Name:           docker-compose
Version:        2.12.2
Release:        2%{?dist}
Summary:        Multi-container orchestration for Docker
Group:          Application/File
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0
URL:            https://github.com/docker/compose

Source0:        https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512  %{name}=dfb82ecc5a984d7193da164924c1e430d07b6378028dac7264b8084da2e315e5c5091803a5db79fe27ed06b002c62b295d873b9371bd19d4550a37a28f8ec952

BuildRequires:  go
BuildRequires:  ca-certificates

%description
Docker Compose (V2) plugin for the Docker CLI.

This plugin provides the 'docker compose' subcommand.

The binary can also be run standalone as a direct replacement for
Docker Compose V1 ('docker-compose').

%prep
%autosetup -p1 -n compose-%{version}

%build
make VERSION=%{version} build %{?_smp_mflags}

%install
install -D -p -m 0755 bin/build/docker-compose %{buildroot}%{_bindir}/docker-compose
for f in LICENSE MAINTAINERS NOTICE README.md; do
    install -D -p -m 0644 "$f" "docker-compose-docs/$f"
done

%if 0%{?with_check}
%check
ver="$(%{buildroot}%{_bindir}/docker-compose docker-cli-plugin-metadata | awk '{ gsub(/[",:]/,"")}; $1 == "Version" { print $2 }')"; \
    test "$ver" = %{version} && echo "PASS: docker-compose version OK" || (echo "FAIL: docker-compose version ($ver) did not match" && exit 1)
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docker-compose-docs/*
%{_bindir}/*

%changelog
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.2-2
- Bump up version to compile with new go
* Wed Nov 2 2022 Gerrit Photon <photon-checkins@vmware.com> 2.12.2-1
- Automatic Version Bump
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-2
- Bump up version to compile with new go
* Mon Sep 19 2022 Mukul Sikka <msikka@vmware.com> 2.11.0-1
- Initial Build
