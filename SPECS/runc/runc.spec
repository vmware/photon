%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        CLI tool for spawning and running containers per OCI spec.
Name:           runc
Version:        1.0.0.rc93
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://runc.io/
Source0:        https://github.com/opencontainers/runc/archive/runc-%{version}.tar.gz
%define sha1    runc=e8693109441696536710e5751e0fee6e6fa32590
# Must be in sync with package version
# Current commit-ID is ahead of git tag for CVE-2021-30465 fix. Remove it after version-bump.
%define RUNC_COMMIT 14faf1c20948688a48edb9b41367ab07ac11ca91
# use major.minor.patch-rcX
%define RUNC_VERSION 1.0.0-rc93
# CVE-2021-30465 patches on top of rc93
Patch0:         runc-rc93-0001-libct-newInitConfig-nit.patch
Patch1:         runc-rc93-0002-libct-rootfs-introduce-and-use-mountConfig.patch
Patch2:         runc-rc93-0003-libct-rootfs-mountCgroupV2-minor-refactor.patch
Patch3:         runc-rc93-0004-Fix-cgroup2-mount-for-rootless-case.patch
Patch4:         runc-rc93-0005-rootfs-add-mount-destination-validation.patch

%define RUNC_BRANCH v%{RUNC_VERSION}
%define gopath_comp github.com/opencontainers/runc
Group:          Virtualization/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  which
BuildRequires:  go-md2man
BuildRequires:  pkg-config
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel

%description
runC is a CLI tool for spawning and running containers according to the OCI specification. Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%package        doc
Summary:        Documentation for runc
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation for runc

%prep
%setup -q -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{RUNC_VERSION} src/%{gopath_comp}
cd src/%{gopath_comp}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make %{?_smp_mflags} GIT_BRANCH=%{RUNC_BRANCH} COMMIT_NO=%{RUNC_COMMIT} COMMIT=%{RUNC_COMMIT} BUILDTAGS='seccomp apparmor' EXTRA_LDFLAGS=-w runc man

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
make DESTDIR=%{buildroot} PREFIX=%{_prefix} BINDIR=%{_bindir} install install-bash install-man

%files
%defattr(-,root,root)
%{_bindir}/runc
%{_datadir}/bash-completion/completions/runc
%{_datadir}/licenses/%{name}

%files doc
%doc
%{_mandir}/man8/*

%changelog
*   Fri May 14 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-2
-   Fix for CVE-2021-30465
*   Wed May 05 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-1
-   Bump up version to 1.0.0-rc93 for containerd
*   Fri Nov 20 2020 Ankit Jain <ankitja@vmware.com> 1.0.0.rc10-1
-   Updated to 1.0.0.rc10
*   Thu Aug 20 2020 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc9-4
-   Fix CVE-2019-19921
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.0.0.rc9-3
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.0.0.rc9-2
-   Bump up version to compile with new go
*   Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 1.0.0.rc9-1
-   Bump up version to 1.0.0-rc9 for containerd
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.1.1-4
-   Bump up version to compile with new go
*   Mon Feb 11 2019 Bo Gan <ganb@vmware.com> 0.1.1-3
-   Fix CVE-2019-5736
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.1-2
-   Add iptables-devel to BuildRequires
*   Tue Apr 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.1-1
-   Initial runc package for PhotonOS.
