%global debug_package   %{nil}
%define plugins_dir     %{_libexecdir}/docker/cli-plugins

Name:           docker-compose
Version:        2.20.2
Release:        6%{?dist}
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
%make_build VERSION=%{version} build

%install
install -D -p -m 0755 ./bin/build/%{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{plugins_dir}
ln -srv %{buildroot}%{_bindir}/%{name} %{buildroot}%{plugins_dir}/

for f in LICENSE MAINTAINERS NOTICE README.md; do
    install -D -p -m 0644 "$f" "%{name}-docs/$f"
done

%check
ver="$(%{buildroot}%{_bindir}/%{name} docker-cli-plugin-metadata | awk '{ gsub(/[",:]/,"")}; $1 == "Version" { print $2 }')"; \
    test "$ver" = %{version} && echo "PASS: %{name} version OK" || (echo "FAIL: %{name} version ($ver) did not match" && exit 1)

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{name}-docs/*
%{_bindir}/%{name}
%{plugins_dir}/%{name}

%changelog
* Fri Oct 25 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.20.2-6
- Create a sym link to make `docker compose` work.
* Mon Jun 24 2024 Mukul Sikka <msikka@vmware.com> 2.20.2-5
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-4
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-3
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-2
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-1
- Upgrade to 2.20.2.
* Fri Jun 23 2023 Piyush Gupta <gpiyush@vmware.com> 2.19.0-1
- Upgrade to v2.19.0.
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-7
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-6
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-5
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-4
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-2
- Bump up version to compile with new go
* Mon Sep 19 2022 Mukul Sikka <msikka@vmware.com> 2.11.0-1
- Initial Build
