%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        Containerd
Name:           containerd
Version:        1.3.10
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://containerd.io/docs/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/containerd/containerd/archive/containerd-%{version}.tar.gz
%define sha1 containerd=a1173daed7f546a0f1fba18c3dc5ce59989c8f53
# Must be in sync with package version
%define CONTAINERD_GITCOMMIT 1c5970efbdd8bc864a34baa60c0b382434d4d7c2

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
Requires:       runc = 1.0.0.rc10

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
%{_bindir}/containerd-shim-runc-v2
%{_bindir}/containerd-stress

%files doc
%defattr(-,root,root)
%doc
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
*   Mon Mar 22 2021 Ankit Jain <ankitja@vmware.com> 1.3.10-1
-   Update to 1.3.10 to fix CVE-2021-21334
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.3.9-3
-   Bump up version to compile with new go
*   Tue Dec 1 2020 HarinadhD <hdommaraju@vmware.com> 1.3.9-2
-   Bump up version to compile with new go
*   Mon Nov 30 2020 Bo Gan <ganb@vmware.com> 1.3.9-1
-   Update to 1.3.9 for upstream fix of CVE-2020-15257
*   Fri Nov 20 2020 Ankit Jain <ankitja@vmware.com> 1.3.7-1
-   Update to 1.3.7 to fix CVE-2020-15257
*   Fri Oct 16 2020 Ashwin H <ashwinh@vmware.com> 1.2.14-1
-   Update to 1.2.14 to fix CVE-2020-15157
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.10-3
-   enable critical restart
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.10-2
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 1.2.10-1
-   Bump up version to 1.2.10 and cleanups
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.8-2
-   Bump up version to compile with go 1.13.3
*   Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
-   Initial version of containerd spec.
