%global debug_package %{nil}

%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        Configures network interfaces in cloud enviroment
Name:           cloud-network-setup
Version:        0.2.2
Release:        7%{?dist}
License:        Apache-2.0
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/%{name}/archive/refs/tags/v%{version}.tar.gz

Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=bf1e917dc016e46dbb3012dc3603f8e24696ce26e9a671bcc98d8d248312bcbb7f5711c4344f230bda374b3c00c8f63121e420ea75110f032acdd43b4ff47882

BuildRequires:  go
BuildRequires:  systemd-rpm-macros

Requires:  systemd

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
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 0.2.2-7
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-6
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-5
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-4
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-2
- Bump up version to compile with new go
* Thu Mar 23 2023 Nitesh Kumar <kunitesh@vmware.com> 0.2.2-1
- Version upgrade to v0.2.2
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-9
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-8
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-6
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-5
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-4
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-3
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-2
-   Bump up version to compile with new go
* Thu Mar 03 2022 Susant Sahani <ssahani@vmware.com> 0.2.1-1
- Version bump.
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.2-3
- Bump up version to compile with new go
* Tue Feb 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.2-2
- Bump up version to compile with new go
* Sun Feb 13 2022 Susant Sahani <ssahani@vmware.com> 0.2-1
- Version bump.
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.1-2
- Bump up version to compile with new go
* Wed Jun 30 2021 Susant Sahani <ssahani@vmware.com> 0.1-1
- Initial rpm release.
