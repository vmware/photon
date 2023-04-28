%define debug_package %{nil}
%define __os_install_post %{nil}

# use major.minor.patch-rcX
%define RUNC_VERSION 1.1.4
%define RUNC_BRANCH  v%{RUNC_VERSION}
%define gopath_comp  github.com/opencontainers/runc

Summary:             CLI tool for spawning and running containers per OCI spec.
Name:                runc
Version:             1.1.4
Release:             3%{?dist}
License:             ASL 2.0
URL:                 https://runc.io
Group:               Virtualization/Libraries
Vendor:              VMware, Inc.
Distribution:        Photon
Source0:             https://github.com/opencontainers/runc/archive/%{name}-%{version}.tar.gz
%define sha512       %{name}=c8e79ad839964680d29ab56a4de255f91192741951673025da6889c544a232d4d392db2da8005d8e22999a37bfbc9c9fe7f6043b165bc4edc2f2a29261d8a3d6
BuildRequires:       go
BuildRequires:       which
BuildRequires:       go-md2man
BuildRequires:       pkg-config
BuildRequires:       libseccomp
BuildRequires:       libseccomp-devel

%description
runC is a CLI tool for spawning and running containers according to the OCI specification.
Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%package             doc
Summary:             Documentation for runc
Requires:            %{name} = %{version}-%{release}

%description         doc
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
