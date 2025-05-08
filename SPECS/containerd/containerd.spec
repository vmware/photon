%define debug_package %{nil}
%define __os_install_post %{nil}
%define gopath_comp github.com/%{name}/%{name}

Summary:        Containerd
Name:           containerd
Version:        1.6.38
Release:        1%{?dist}
URL:            https://containerd.io/docs
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/containerd/archive/refs/tags/v%{version}.tar.gz

# Must be in sync with package version
%define CONTAINERD_GITCOMMIT cf158e884cfe4812a6c371b59e4ea9bc4c46e51a

Source1: %{name}-config.toml
Source2: disable-%{name}-by-default.preset

Source3: license.txt
%include %{SOURCE3}

Patch0: %{name}-service.patch
Patch1: build-bin-gen-manpages-instead-of-using-go-run.patch

BuildRequires: btrfs-progs
BuildRequires: btrfs-progs-devel
BuildRequires: libseccomp
BuildRequires: libseccomp-devel
BuildRequires: go >= 1.23
BuildRequires: go-md2man
BuildRequires: systemd-devel

Requires: libseccomp
Requires: systemd
# containerd 1.4.5 and above allow to use runc 1.0.0-rc94 and above.
# refer to v1.4.5/RUNC.md
Requires: runc

%description
Containerd is an open source project. It is available as a daemon for Linux,
which manages the complete container lifecycle of its host system.

%package        extras
Summary:        Extra binaries for containerd
Group:          Applications/File
Requires:       %{name} = %{version}-%{release}

%description extras
Extra binaries for containerd

%package        doc
Summary:        containerd
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for containerd.

%prep
# Using autosetup is not feasible
%setup -q -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
cd %{name}-%{version}
%autopatch -p1
cd ..
mv %{name}-%{version} src/%{gopath_comp}

%build
export GOPATH="${PWD}"
# We still have to use the GOPATH mode, as containerd only supports go.mod
# starting 1.5.0+ However, this mode might be soon removed --
# https://github.com/golang/go/wiki/GOPATH

# Also, attempting to create go.mod and re-vendor would be wrong in this case,
# as it could overwrite patches to vendor/, as well as fetching un-release
# upstream versions. Typically, embargoed CVEs can cause those versions to be hiddden.
export GO111MODULE=off
cd src/%{gopath_comp}

make %{?_smp_mflags} VERSION=%{version} REVISION=%{CONTAINERD_GITCOMMIT} \
         BUILDTAGS='seccomp selinux apparmor' binaries man

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
install -v -m644 -D -t %{buildroot}%{_unitdir} %{name}.service
install -v -m644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/config.toml
install -v -m644 -D %{SOURCE2} %{buildroot}%{_presetdir}/50-%{name}.preset
make %{?_smp_mflags} DESTDIR=%{buildroot} PREFIX=%{_prefix} install
make %{?_smp_mflags} DESTDIR=%{buildroot} PREFIX=%{_prefix} install-man

%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%preun
%systemd_preun %{name}.service

%clean
rm -rf %{buildroot}/*

%if 0%{?with_check}
%check
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make %{?_smp_mflags} test
make %{?_smp_mflags} root-test
make %{?_smp_mflags} integration
%endif

%files
%defattr(-,root,root)
%{_bindir}/ctr
%{_bindir}/%{name}
%{_bindir}/%{name}-shim
%{_datadir}/licenses/%{name}
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%config(noreplace) %{_sysconfdir}/%{name}/config.toml

%files extras
%defattr(-,root,root)
%{_bindir}/%{name}-shim-runc-v1
%{_bindir}/%{name}-shim-runc-v2
%{_bindir}/%{name}-stress

%files doc
%defattr(-,root,root)
%doc
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Thu May 08 2025 Akhil Mohan <akhil.mohan@broadcom.com> 1.6.38-1
- Upgrade to 1.6.38
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.6.21-13
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.6.21-12
- Bump version as a part of go upgrade
* Tue Sep 10 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.6.21-11
- Bump up version as a part of runc upgrade to v1.1.14
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.6.21-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.6.21-9
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.6.21-8
- Bump version as a part of go upgrade
* Tue Feb 06 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.6.21-7
- Bump up version as a part of runc upgrade to v1.1.12
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.21-6
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.21-5
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.21-4
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.21-3
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.21-2
- Bump up version to compile with new go
* Fri May 19 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.21-1
- Upgrade to v1.6.21.
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.17-4
- Bump up version to compile with new go
* Fri Apr 28 2023 Nitesh Kumar <kunitesh@vmware.com> 1.6.17-3
- Version bump up to use latest runc v1.1.7
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.17-2
- Bump up version to compile with new go
* Fri Feb 10 2023 Gerrit Photon <photon-checkins@vmware.com> 1.6.17-1
- Automatic Version Bump
* Wed Nov 30 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.9-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.6-6
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.6-5
- Bump up version to compile with new go
* Thu Sep 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.6.6-4
- Restore GO111MODULE to off.
* Mon Aug 8 2022 Shivani Agarwal <shivania2@vmware.com> 1.6.6-3
- Enable selinux
* Sun Jul 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.6-2
- Bump up version to compile with new go.
* Wed Jul 20 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 1.6.6-1
- Update to version 1.6.6
* Mon Dec 13 2021 Nitesh Kumar <kunitesh@vmware.com> 1.4.12-1
- Upgrading to 1.4.12 to use latest runc.
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.4-2
- Bump up version to compile with new go
* Mon Mar 22 2021 Ankit Jain <ankitja@vmware.com> 1.4.4-1
- Update to 1.4.4
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.4.1-4
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.1-3
- Bump up version to compile with new go
* Wed Oct 07 2020 Tapas Kundu <tkundu@vmware.com> 1.4.1-2
- Use latest runc
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.1-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
- Initial version of containerd spec.
