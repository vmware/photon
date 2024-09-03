%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        A terminal user-interface for tshark, inspired by Wireshark
Name:           termshark
Version:        2.2.0
Release:        22%{?dist}
License:        MIT
URL:            https://github.com/gcla/%{name}/releases/tag/v%{version}.tar.gz
Source0:        termshark-%{version}.tar.gz
%define sha512  %{name}=5ab2e2ccb7d4ab71a5b364c9677a24725dc5702a1c574f93ec2f4f09aba2322c292728f9ea02eb1d7378e7ea32ee4952dc59fd7b699e70fcaa3007c1f28219db
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
%{_bindir}/termshark

%changelog
* Tue Sep 03 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.2.0-22
- Version bump up to consume wireshark v4.2.7
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.2.0-21
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.2.0-20
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 2.2.0-19
- Bump version as a part of go upgrade
* Mon Apr 01 2024 Anmol Jain <anmol.jain@broadcom.com> 2.2.0-18
- Bump version as a part of wireshark upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-17
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-16
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-15
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-14
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-13
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-12
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-11
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-10
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-9
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-8
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-7
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-6
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-5
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-4
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-3
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 2.2.0-2
-   Bump up version to compile with new go
* Thu May 06 2021 Susant Sahani <ssahani@vmware.com> 2.2.0-1
- Initial rpm release.
