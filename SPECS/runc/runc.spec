%define debug_package %{nil}
%define __os_install_post %{nil}

# use major.minor.patch-rcX
%define RUNC_VERSION 1.1.14
%define RUNC_BRANCH  v%{RUNC_VERSION}
%define gopath_comp  github.com/opencontainers/runc

Summary:             CLI tool for spawning and running containers per OCI spec.
Name:                runc
Version:             1.1.14
Release:             1%{?dist}
License:             GNU LGPL v2.1
URL:                 https://runc.io
Group:               Virtualization/Libraries
Vendor:              VMware, Inc.
Distribution:        Photon

Source0: https://github.com/opencontainers/runc/archive/runc-%{version}.tar.gz
%define sha512 %{name}=bdefbf34cf57485c6b961babc8294d0e6b2e003eb836b8e99c49ef4d00acf11f30a46ad0bcd399ee9346610419591daf1eecb3b6b127962357d629bf5f252e22

BuildRequires: go
BuildRequires: which
BuildRequires: go-md2man
BuildRequires: pkg-config
BuildRequires: libseccomp
BuildRequires: libseccomp-devel

%description
runC is a CLI tool for spawning and running containers according to the OCI specification.
Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%package     doc
Summary:     Documentation for runc
Requires:    %{name} = %{version}-%{release}

%description doc
Documentation for runc

%prep
%autosetup -p1 -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{RUNC_VERSION} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make %{?_smp_mflags} GIT_BRANCH=%{RUNC_BRANCH} BUILDTAGS='seccomp selinux apparmor' EXTRA_LDFLAGS=-w %{name} man

%install
cd src/%{gopath_comp}
#BINDIR is pointing to absolute path so DESTDIR is not required.
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
make %{?_smp_mflags} DESTDIR="" PREFIX=%{buildroot}%{_prefix} BINDIR=%{buildroot}%{_bindir} install install-bash install-man

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/licenses/%{name}

%files doc
%doc
%{_mandir}/man8/*

%changelog
* Tue Sep 10 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.1.14-1
- Version upgrade to v1.1.14 to address CVE-2024-45310
* Tue Feb 06 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.1.12-1
- Version upgrade to v1.1.12 to fix CVE-2024-21626
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.7-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.7-6
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.7-5
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.7-4
- Bump up version to compile with new go
* Mon Jul 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.7-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.7-2
- Bump up version to compile with new go
* Fri Apr 28 2023 Nitesh Kumar <kunitesh@vmware.com> 1.1.7-1
- Version upgrade to v1.1.7 to fix following issue:
- 1461 (broken NVidia device support)
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-3
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.4-2
- Bump up version to compile with new go
* Thu Nov 03 2022 Nitesh Kumar <kunitesh@vmware.com> 1.1.4-1
- Version upgrade to v1.1.4
* Tue Jul 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-2
- Bump up version to compile with new go
* Tue Jun 07 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.3-1
- Automatic Version Bump
* Sat May 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.1-1
- Upgrade to v1.1.1 & enable selinux in BUILDTAGS
* Mon Dec 13 2021 Nitesh Kumar <kunitesh@vmware.com> 1.0.3-1
- Version upgrade to fix CVE-2021-43784.
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0.rc92-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.0.0.rc92-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0.rc92-2
- Bump up version to compile with new go
* Tue Oct 06 2020 Tapas Kundu <tkundu@vmware.com> 1.0.0.rc92-1
- Updated to rc92
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.0.rc9-1
- Automatic Version Bump
- it is manually updated with containerd
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 1.0.0.rc8-2
- Build with python3
- Mass removal python2
* Thu Jun 13 2019 Tapas Kundu <tkundu@vmware.com> 1.0.0.rc8-1
- Update to release 1.0.0-rc8
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.1-2
- Add iptables-devel to BuildRequires
* Tue Apr 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.1-1
- Initial runc package for PhotonOS.
