%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        A terminal user-interface for tshark, inspired by Wireshark
Name:           termshark
Version:        2.4.0
Release:        13%{?dist}
License:        MIT
URL:            https://github.com/gcla/%{name}/releases/tag/v%{version}.tar.gz
Source0:        https://github.com/gcla/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=378bb67ff50a8dfa80f614540371f326627e73bdf63bceb183ed73afbbf9dead4e0597fb969ba49c4ee3d3de00ac7bb91166421c19c788df47ff8d9fcbc5b9fc

Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
BuildRequires:  wireshark-devel
BuildRequires:  libpcap-devel
Requires:       wireshark
Requires:       libpcap

%global debug_package %{nil}

%description
Termshark is the terminal user-interface tor Tshark, a source network protocol analyzer.
TShark doesn't have an interactive terminal user interface though, and this is where
Termshark comes in. Termshark is basically the futuristic terminal version of Wireshark.

%prep -p exit
%autosetup -p1 -n %{name}-%{version}

%build
export ARCH=%{gohostarch}
export VERSION=%{version}
export PKG=github.com/%{name}/%{name}
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GOBIN=/usr/share/gocode/bin
export PATH=$PATH:$GOBIN

mkdir -p ${GOPATH}/src/${PKG}
cp -rf . ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}
go build -v ./cmd/...
popd

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/termshark

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.4.0-13
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.4.0-12
- Bump version as a part of go upgrade
* Mon Apr 01 2024 Anmol Jain <anmol.jain@broadcom.com> 2.4.0-11
- Bump version as a part of wireshark upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 2.4.0-10
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-9
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-8
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-7
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-6
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-5
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-4
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-3
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.4.0-2
- Bump up version to compile with new go
* Tue Nov 1 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.0-1
- Automatic Version Bump
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-2
- Bump up version to compile with new go
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 2.3.0-1
- Version bump.
* Thu May 06 2021 Susant Sahani <ssahani@vmware.com> 2.2.0-1
- Initial rpm release.
