%define debug_package %{nil}
%define __os_install_post %{nil}
# use major.minor.patch-rcX
%define RUNC_VERSION 1.0.3
%define RUNC_BRANCH  v%{RUNC_VERSION}
%define gopath_comp  github.com/opencontainers/runc
Summary:             CLI tool for spawning and running containers per OCI spec.
Name:                runc
Version:             1.0.3
Release:             1%{?dist}
License:             ASL 2.0
URL:                 https://runc.io/
Source0:             https://github.com/opencontainers/runc/archive/runc-%{version}.tar.gz
%define sha1         runc=cbd1b1eff60b0d6f61a034cb50a7fe22edd2b140

Group:               Virtualization/Libraries
Vendor:              VMware, Inc.
Distribution:        Photon
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
cd src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make %{?_smp_mflags} GIT_BRANCH=%{RUNC_BRANCH} BUILDTAGS='seccomp apparmor' EXTRA_LDFLAGS=-w runc man

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
make DESTDIR=%{buildroot} PREFIX=%{_prefix} BINDIR=%{_bindir} install install-bash install-man %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/runc
%{_datadir}/bash-completion/completions/runc
%{_datadir}/licenses/%{name}

%files doc
%doc
%{_mandir}/man8/*

%changelog
*   Mon Dec 13 2021 Nitesh Kumar <kunitesh@vmware.com> 1.0.3-1
-   Version upgrade to fix CVE-2021-43784.
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-5
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-4
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-3
-   Bump up version to compile with new go
*   Fri May 14 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-2
-   Fix for CVE-2021-30465
*   Wed May 05 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-1
-   Bump up version to 1.0.0-rc93
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0.rc92-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.0.0.rc92-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0.rc92-2
-   Bump up version to compile with new go
*   Tue Oct 06 2020 Tapas Kundu <tkundu@vmware.com> 1.0.0.rc92-1
-   Updated to rc92
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.0.rc9-1
-   Automatic Version Bump
-   it is manually updated with containerd
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 1.0.0.rc8-2
-   Build with python3
-   Mass removal python2
*   Thu Jun 13 2019 Tapas Kundu <tkundu@vmware.com> 1.0.0.rc8-1
-   Update to release 1.0.0-rc8
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.1-2
-   Add iptables-devel to BuildRequires
*   Tue Apr 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.1-1
-   Initial runc package for PhotonOS.
