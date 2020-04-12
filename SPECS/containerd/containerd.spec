%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        Containerd
Name:           containerd
Version:        1.2.10
Release:        3%{?dist}
License:        ASL 2.0
URL:            https://containerd.io/docs/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/containerd/containerd/archive/containerd-%{version}.tar.gz
%define sha1 containerd=711c6bf96ab9b6a13a641643b4c96b3b8261ffb0
# Must be in sync with package version
%define CONTAINERD_GITCOMMIT b34a5c8af56e510852c35414db4c1f4fa6172339

Source1:        containerd.service
Source2:        containerd-config.toml
Source3:        disable-containerd-by-default.preset
%define gopath_comp github.com/containerd/containerd

BuildRequires:  btrfs-progs
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  go >= 1.10.7
BuildRequires:  go-md2man
BuildRequires:  systemd-devel
Requires:       libseccomp
Requires:       systemd
# containerd works only with a specific runc version
# Refer to containerd/RUNC.md
Requires:       runc = 1.0.0.rc9

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
mv %{name}-%{version} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make %{?_smp_mflags} VERSION=%{version} REVISION=%{CONTAINERD_GITCOMMIT} binaries man

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
install -v -m644 -D -t %{buildroot}%{_unitdir} %{SOURCE1}
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
%{_bindir}/containerd-stress

%files doc
%defattr(-,root,root)
%doc
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.10-3
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.2.10-2
-   Bump up version to compile with new go
*   Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 1.2.10-1
-   Bump up version to 1.2.10 and cleanups
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.8-2
-   Bump up version to compile with go 1.13.3
*   Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
-   Initial version of containerd spec.
