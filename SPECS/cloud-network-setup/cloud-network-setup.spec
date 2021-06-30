%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        Configures network interfaces in cloud enviroment
Name:           cloud-network-setup
Version:        0.1
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        cloud-network-setup-%{version}.tar.gz
%define sha1 %{name}=e7c39df9c0b389c0c1b2a53516ce3ec738018008
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  go
BuildRequires:  systemd-rpm-macros

Requires:  systemd

%global debug_package %{nil}

%description
cloud-network configures network in cloud environment. In cloud environment
instances are set public IPs and private IPs. If more than one private IP is
configured then except the IP which is provided by DHCP others can't be fetched
and configured. This project is adopting towards cloud network environment such
as Azure, GCP and Amazon EC2.
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

go build -o bin/cloud-network ./cmd/cloud-network
go build -o bin/cnctl ./cmd/cnctl

popd

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/cloud-network
install -m 755 -d %{buildroot}%{_unitdir}

install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/bin/cloud-network
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/bin/cnctl

install -pm 755 -t %{buildroot}%{_sysconfdir}/cloud-network ${GOPATH}/src/github.com/%{name}/%{name}/distribution/cloud-network.toml
install -pm 755 -t %{buildroot}%{_unitdir}/ ${GOPATH}/src/github.com/%{name}/%{name}/distribution/cloud-network.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/cloud-network
%{_bindir}/cnctl

%{_sysconfdir}/cloud-network/cloud-network.toml
%{_unitdir}/cloud-network.service

%pre
if ! getent group cloud-network >/dev/null 2>&1; then
    /usr/sbin/groupadd -g 89 cloud-network
fi

if ! getent passwd cloud-network >/dev/null 2>&1 ; then
    /usr/sbin/useradd -g 89 -u 89 -r -s /sbin/nologin cloud-network >/dev/null 2>&1 || exit 1
fi

%post
%systemd_post cloud-network.service

%preun
%systemd_preun cloud-network.service

%postun
%systemd_postun_with_restart cloud-network.service

%changelog
* Wed Jun 30 2021 Susant Sahani <ssahani@vmware.com> 0.1-1
- Initial rpm release.
