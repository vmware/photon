%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        A terminal user-interface for tshark, inspired by Wireshark
Name:           termshark
Version:        2.3.0
Release:        3%{?dist}
License:        MIT
URL:            https://github.com/gcla/%{name}/releases/tag/v%{version}.tar.gz
Source0:        https://github.com/gcla/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=0ed780ec1ba86d2a6eb11c940f00475c750075d5e1ae4a6022f465572717126df941e933e2db7123d802b721f8e1187014f02d4c5dfd84c1a55009045dce5a88
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
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-2
- Bump up version to compile with new go
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 2.3.0-1
- Version bump.
* Thu May 06 2021 Susant Sahani <ssahani@vmware.com> 2.2.0-1
- Initial rpm release.
