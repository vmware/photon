%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        pm-webd is an open source, super light weight remote management API Gateway
Name:           pmweb
Version:        1.0
Release:        2%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        pmweb-%{version}.tar.gz
%define sha1 %{name}=557b264a76ea4002d28e5f75f7879fd0bbfa8f1c
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  glibc
BuildRequires:  go
BuildRequires:  systemd-rpm-macros

Requires:  systemd

%global debug_package %{nil}

%description
pm-webd is a high performance open-source, simple, and pluggable REST API gateway
designed with stateless architecture.It is written in Go, and built with performance in mind.
It features real time health monitoring, configuration and performance for systems (containers),
networking and applications.

%prep -p exit
%autosetup -p1 -n %{name}

%build
mkdir -p bin
go build -ldflags="-X 'main.buildVersion=${VERSION}' -X 'main.buildDate=${BUILD_DATE}'" -o bin/pm-webd ./cmd/pmweb
go build -ldflags="-X 'main.buildVersion=${VERSION}' -X 'main.buildDate=${BUILD_DATE}'" -o bin/pmctl ./cmd/pmctl

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/pm-web
install -m 755 -d %{buildroot}%{_unitdir}

install bin/pm-webd %{buildroot}%{_bindir}
install bin/pmctl %{buildroot}%{_bindir}
install -m 755 conf/pmweb.toml %{buildroot}%{_sysconfdir}/pm-web
install -m 755 conf/pmweb-auth.conf %{buildroot}%{_sysconfdir}/pm-web

install -m 0644 units/pm-webd.service %{buildroot}%{_unitdir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/pm-webd
%{_bindir}/pmctl

%{_sysconfdir}/pm-web/pmweb.toml
%config(noreplace) %{_sysconfdir}/pm-web/pmweb-auth.conf
%{_unitdir}/pm-webd.service

%pre
if ! getent group pm-web >/dev/null; then
    /sbin/groupadd -r pm-web
fi

if ! getent passwd pm-web >/dev/null; then
    /sbin/useradd -g pm-web pm-web -s /sbin/nologin
fi

%post
%systemd_post pm-webd.service

%preun
%systemd_preun pm-webd.service

%postun
%systemd_postun_with_restart pm-webd.service

if [ $1 -eq 0 ] ; then
    if getent passwd pm-web >/dev/null; then
        /sbin/userdel pm-web
    fi
    if getent group pm-web >/dev/null; then
        /sbin/groupdel pm-web
    fi
fi

%changelog
* Tue Dec 14 2021 Susant Sahani <ssahani@vmware.com> 1.0-2
- Create pm-user
* Wed Nov 17 2021 Harinadh D <hdommaraju@vmware.com> 1.0-1
- Initial rpm release.
