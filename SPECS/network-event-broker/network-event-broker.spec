%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        Manages network configuration
Name:           network-event-broker
Version:        0.3
Release:        9%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/%{name}
Source0:        https://github.com/vmware/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=3560c1e25b0df04071b43492d9b043140d95c05fe96a1216ae19992965b99c0bef23141771c1f1d36b7af8ea1772d2d222011705c2321ac42ee408ee19647b2d
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  go
BuildRequires:  systemd-rpm-macros

Requires:         systemd
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

%global debug_package %{nil}

%description
A daemon that configures the network and executes scripts on network events such as
systemd-networkd's DBus events or dhclient gaining a lease. It also watches
when an address gets added/removed/modified or links get added/removed.

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
go build -o bin/network-broker ./cmd/network-broker
popd

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/network-broker
install -m 755 -d %{buildroot}%{_unitdir}

install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/bin/network-broker

install -pm 755 -t %{buildroot}%{_sysconfdir}/network-broker ${GOPATH}/src/github.com/%{name}/%{name}/distribution/network-broker.toml
install -pm 755 -t %{buildroot}%{_unitdir}/ ${GOPATH}/src/github.com/%{name}/%{name}/distribution/network-broker.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/network-broker

%{_sysconfdir}/network-broker/network-broker.toml
%{_unitdir}/network-broker.service

%pre
if ! getent group network-broker >/dev/null; then
    /sbin/groupadd -r network-broker
fi

if ! getent passwd network-broker >/dev/null; then
    /sbin/useradd -g network-broker network-broker -s /sbin/nologin
fi

%post
%systemd_post network-broker.service

%preun
%systemd_preun network-broker.service

%postun
%systemd_postun_with_restart network-broker.service

if [ $1 -eq 0 ] ; then
    if getent passwd network-broker >/dev/null; then
        /sbin/userdel network-broker
    fi

    if getent group network-broker >/dev/null; then
        /sbin/groupdel network-broker
    fi
fi

%changelog
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.3-9
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 0.3-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-6
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-5
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-3
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-2
- Bump up version to compile with new go
* Wed Jan 11 2023 Nitesh Kumar <kunitesh@vmware.com> 0.3-1
- Version upgrade to v0.3
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-10
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-8
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-7
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-6
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-5
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-4
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-3
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-2
-   Bump up version to compile with new go
* Wed Dec 22 2021 Susant Sahani <ssahani@vmware.com> 0.2.1-1
- Version bump and add groupadd and useradd to requires.
* Tue Dec 14 2021 Susant Sahani <ssahani@vmware.com> 0.2-1
- Version bump.
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.1-2
- Bump up version to compile with new go
* Wed Jun 30 2021 Susant Sahani <ssahani@vmware.com> 0.1-1
- Initial rpm release.
