Summary:	CLI tool for spawning and running containers per OCI spec.
Name:		runc
Version:	1.0.0.rc93
Release:	1%{?dist}
License:	ASL 2.0
URL:		https://runc.io/
Source0:        https://github.com/opencontainers/runc/archive/runc-%{version}.tar.gz
%define sha1    runc=e8693109441696536710e5751e0fee6e6fa32590
# Must be in sync with package version
%define RUNC_COMMIT 12644e614e25b05da6fd08a38ffa0cfe1903fdec
# use major.minor.patch-rcX
%define RUNC_VERSION 1.0.0-rc93

%define RUNC_BRANCH v%{RUNC_VERSION}
%define gopath_comp github.com/opencontainers/runc
Group:		Virtualization/Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  which
BuildRequires:  go
BuildRequires:  pkg-config
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel

%description
runC is a CLI tool for spawning and running containers according to the OCI specification. Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%prep
%setup -q -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{RUNC_VERSION} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make %{?_smp_mflags} GIT_BRANCH=%{RUNC_BRANCH} COMMIT_NO=%{RUNC_COMMIT} COMMIT=%{RUNC_COMMIT} BUILDTAGS='seccomp'

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
make DESTDIR=%{buildroot} PREFIX=%{_prefix} BINDIR=%{_bindir} install install-bash

%files
%defattr(-,root,root)
%{_bindir}/runc
%{_datadir}/bash-completion/completions/runc
%{_datadir}/licenses/%{name}

%changelog
*   Fri May 14 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-1
-   Bump up version to 1.0.0-rc93 for docker/containerd
*   Fri Apr 24 2020 Harinadh D <hdommaraju@vmware.com> 1.0.0.rc9-2
-   Bump up version to compile with new go version
*   Wed Apr 22 2020 Ankit Jain <ankitja@vmware.com> 1.0.0.rc9-1
-   Updated to 1.0.0.rc9
*   Fri Jan 03 2020 Ashwin H <ashwinh@vmware.com> 1.0.0.rc4-5
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.0.0.rc4-4
-   Bump up version to compile with new go
*   Fri Feb 15 2019 Keerthana K <keerthanak@vmware.com> 1.0.0.rc4-3
-   Rename CVE-2019-5736 patch file.
*   Mon Feb 11 2019 Bo Gan <ganb@vmware.com> 1.0.0.rc4-2
-   Fix CVE-2019-5736
*   Tue Aug 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.0.rc4-1
-   Update runc package to 1.0.0.rc4.
*   Tue Apr 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.1-1
-   Initial runc package for PhotonOS.
