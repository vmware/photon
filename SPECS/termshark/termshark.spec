%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        A terminal user-interface for tshark, inspired by Wireshark
Name:           termshark
Version:        2.3.0
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/gcla/%{name}/releases/tag/v%{version}.tar.gz
Source0:        termshark-%{version}.tar.gz
%define sha1 %{name}=95b1860f724024d15c321ff8d492a36aaa2058e8
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
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 2.3.0-1
- Version bump.
* Thu May 06 2021 Susant Sahani <ssahani@vmware.com> 2.2.0-1
- Initial rpm release.
