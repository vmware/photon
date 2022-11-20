%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        pmd-nextgen is an open source, super light weight remote management API Gateway
Name:           pmd-nextgen
Version:        1.0.1
Release:        3%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        pmd-nextgen-%{version}.tar.gz
%define sha512  %{name}=daa7cf9f708355274d34705f31910d2ca463b94815b7a7c3d4d47e13afb0694eb816e20e7005199862b690021a76a21370bc649f824681777d27796c5d26f908
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  glibc
BuildRequires:  git
BuildRequires:  go
BuildRequires:  systemd-rpm-macros

Requires:  systemd
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel
Requires:  glibc
Obsoletes: pmd
%global debug_package %{nil}

%description
pmd-nextgen is a high performance open-source, simple, and pluggable REST API gateway
designed with stateless architecture.It is written in Go, and built with performance in mind.
It features real time health monitoring, configuration and performance for systems (containers),
networking and applications.

%prep -p exit
%autosetup -p1 -n pmd-%{version}

%build
mkdir -p bin
go build -buildmode=pie -ldflags="-X 'main.buildVersion=${VERSION}' -X 'main.buildDate=${BUILD_DATE}'" -o bin/photon-mgmtd ./cmd/photon-mgmt
go build -ldflags="-X 'main.buildVersion=${VERSION}' -X 'main.buildDate=${BUILD_DATE}'" -o bin/pmctl ./cmd/pmctl

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/photon-mgmt
install -m 755 -d %{buildroot}%{_unitdir}

install bin/photon-mgmtd %{buildroot}%{_bindir}
install bin/pmctl %{buildroot}%{_bindir}
install -m 755 distribution/photon-mgmt.toml %{buildroot}%{_sysconfdir}/photon-mgmt

install -m 0644 units/photon-mgmtd.service %{buildroot}%{_unitdir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/photon-mgmtd
%{_bindir}/pmctl

%{_sysconfdir}/photon-mgmt/photon-mgmt.toml
%{_unitdir}/photon-mgmtd.service

%pre
if ! getent group photon-mgmt >/dev/null; then
    /sbin/groupadd -r photon-mgmt
fi

if ! getent passwd photon-mgmt >/dev/null; then
    /sbin/useradd -g photon-mgmt photon-mgmt -s /sbin/nologin
fi

%post
%systemd_post photon-mgmtd.service

%preun
%systemd_preun photon-mgmtd.service

%postun
%systemd_postun_with_restart photon-mgmtd.service

if [ $1 -eq 0 ] ; then
    if getent passwd photon-mgmt >/dev/null; then
        /sbin/userdel photon-mgmt
    fi
    if getent group photon-mgmt >/dev/null; then
        /sbin/groupdel photon-mgmt
    fi
fi

%changelog
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-2
- Bump up version to compile with new go
* Mon Jun 27 2022 Nitesh Kumar <kunitesh@vmware.com> 1.0.1-1
- Version upgrade to v1.0.1
* Wed Jan 12 2022 Harinadh D <hdommaraju@vmware.com> 1.0-2
- Adding Requires to the package
* Mon Jan 10 2022 Harinadh D <hdommaraju@vmware.com> 1.0-1
- Initial release.
