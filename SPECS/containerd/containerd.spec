%define debug_package %{nil}
%define __os_install_post %{nil}
%define gopath_comp github.com/containerd/containerd
Summary:        Containerd
Name:           containerd
Version:        1.4.4
Release:        5%{?dist}
License:        ASL 2.0
URL:            https://containerd.io/docs/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/containerd/containerd/archive/containerd-%{version}.tar.gz
%define sha1 containerd=0e49f2b0593adc635b89bbcf2d3f40e0fe217933
# Must be in sync with package version
%define CONTAINERD_GITCOMMIT 05f951a3781f4f2c1911b05e61c160e9c30eaa8e

Patch1:         containerd-service-file-binpath.patch
Patch2:         containerd-1.4-Use-chmod-path-for-checking-symlink.patch
Source2:        containerd-config.toml
Source3:        disable-containerd-by-default.preset
BuildRequires:  btrfs-progs
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
# Upstream is unhappy with 1.14. 1.13 or 1.15+ is OK
BuildRequires:  go >= 1.16
BuildRequires:  go-md2man
BuildRequires:  systemd-devel
Requires:       libseccomp
Requires:       systemd
# containerd works only with a specific runc version
# Refer to containerd/RUNC.md
Requires:       runc = 1.0.0.rc93

%description
Containerd is an open source project. It is available as a daemon for Linux,
which manages the complete container lifecycle of its host system.

%package        extras
Summary:        Extra binaries for containerd
Group:          Applications/File
Requires:       %{name} = %{version}-%{release}

%description    extras
Extra binaries for containerd

%package        doc
Summary:        containerd
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation for containerd.

%prep
%setup -q -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
%patch1 -p1 -d %{name}-%{version}
%patch2 -p1 -d %{name}-%{version}
mv %{name}-%{version} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
go mod init
make %{?_smp_mflags} VERSION=%{version} REVISION=%{CONTAINERD_GITCOMMIT} binaries man

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
install -v -m644 -D -t %{buildroot}%{_unitdir} containerd.service
install -v -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/containerd/config.toml
install -v -m644 -D %{SOURCE3} %{buildroot}%{_presetdir}/50-containerd.preset
make DESTDIR=%{buildroot}%{_prefix} install
make DESTDIR=%{buildroot}%{_datadir} install-man

%post
%systemd_post containerd.service

%postun
%systemd_postun_with_restart containerd.service

%preun
%systemd_preun containerd.service

%check
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make test
make root-test
make integration

%files
%defattr(-,root,root)
%{_bindir}/ctr
%{_bindir}/containerd
%{_bindir}/containerd-shim
%{_datadir}/licenses/%{name}
%{_unitdir}/containerd.service
%{_presetdir}/50-containerd.preset
%config(noreplace) %{_sysconfdir}/containerd/config.toml

%files extras
%defattr(-,root,root)
%{_bindir}/containerd-shim-runc-v1
%{_bindir}/containerd-shim-runc-v2
%{_bindir}/containerd-stress

%files doc
%defattr(-,root,root)
%doc
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
*   Fri Jul 16 2021 Bo Gan <ganb@vmware.com> 1.4.4-5
-   Fix CVE-2021-32760
-   Refactor containerd.service patching and installation
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-4
-   Bump up version to compile with new go
*   Thu May 27 2021 Bo Gan <ganb@vmware.com> 1.4.4-3
-   Bump up release version to consume new runc dependency
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.4-2
-   Bump up version to compile with new go
*   Mon Mar 22 2021 Ankit Jain <ankitja@vmware.com> 1.4.4-1
-   Update to 1.4.4
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.4.1-4
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.1-3
-   Bump up version to compile with new go
*   Wed Oct 07 2020 Tapas Kundu <tkundu@vmware.com> 1.4.1-2
-   Use latest runc
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.1-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
-   Automatic Version Bump
*   Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
-   Initial version of containerd spec.
