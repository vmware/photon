%define network_required 1
%global debug_package %{nil}

Name:           docker-compose
Version:        2.20.2
Release:        7%{?dist}
Summary:        Multi-container orchestration for Docker
Group:          Application/File
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0
URL:            https://github.com/docker/compose

Source0:        https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512  %{name}=8b8ccece806edfaffef497ed8b8b64c6050aa35363e350a14b5a257c9230ed5656a0e5661ce6c314c2911b438780421f71714477a83e2e64db2cf6c921f86af1

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
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.20.2-7
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.20.2-6
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 2.20.2-5
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-4
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-3
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-2
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-1
- Upgrade to 2.20.2.
* Fri Jun 23 2023 Piyush Gupta <gpiyush@vmware.com> 2.19.0-1
- Upgrade to v2.19.0.
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.14.0-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.14.0-3
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 2.14.0-2
- Bump up version to compile with new go
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 2.14.0-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.2-2
- Bump up version to compile with new go
* Wed Nov 2 2022 Gerrit Photon <photon-checkins@vmware.com> 2.12.2-1
- Automatic Version Bump
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-2
- Bump up version to compile with new go
* Mon Sep 19 2022 Mukul Sikka <msikka@vmware.com> 2.11.0-1
- Initial Build
