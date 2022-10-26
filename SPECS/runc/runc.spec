%define debug_package %{nil}
%define __os_install_post %{nil}

# Must be in sync with package version
%define RUNC_COMMIT_SHORT f46b6ba
# use major.minor.patch-rcX
%define RUNC_VERSION 1.1.3
%define RUNC_GITTAG v%{RUNC_VERSION}
%define gopath_comp github.com/opencontainers/runc

Summary:        CLI tool for spawning and running containers per OCI spec.
Name:           runc
Version:        1.1.3
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://runc.io/
Source0:        https://github.com/opencontainers/runc/archive/runc-%{version}.tar.gz
%define sha1    runc=9ad2300d41deb361ced92112366d0c8801d00050
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
%autosetup -p1 -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{RUNC_VERSION} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
# Use the format of `git describe --long` as COMMIT
make %{?_smp_mflags} GIT_BRANCH=%{RUNC_GITTAG} COMMIT=%{RUNC_GITTAG}-0-g%{RUNC_COMMIT_SHORT} BUILDTAGS='seccomp apparmor' EXTRA_LDFLAGS=-w runc man

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
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-2
- Bump up version to compile with new go
* Tue Oct 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-1
- Upgrade to v1.1.3.
* Sat Sep 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-6
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-5
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-4
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-3
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-2
- Bump up version to compile with new go
* Fri Feb 25 2022 Bo Gan <ganb@vmware.com> 1.0.3-1
- Update to 1.0.3
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-6
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-5
- Bump up version to compile with new go
* Mon Dec 13 2021 Nitesh Kumar <kunitesh@vmware.com> 1.0.0.rc93-4
- Fix for CVE-2021-43784.
* Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-3
- Bump up version to compile with new go
* Fri May 14 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-2
- Fix for CVE-2021-30465
* Wed May 05 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-1
- Bump up version to 1.0.0-rc93 for containerd
* Fri Nov 20 2020 Ankit Jain <ankitja@vmware.com> 1.0.0.rc10-1
- Updated to 1.0.0.rc10
* Thu Aug 20 2020 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc9-4
- Fix CVE-2019-19921
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.0.0.rc9-3
- Bump up version to compile with go 1.13.5-2
* Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.0.0.rc9-2
- Bump up version to compile with new go
* Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 1.0.0.rc9-1
- Bump up version to 1.0.0-rc9 for containerd
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.1.1-4
- Bump up version to compile with new go
* Mon Feb 11 2019 Bo Gan <ganb@vmware.com> 0.1.1-3
- Fix CVE-2019-5736
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.1-2
- Add iptables-devel to BuildRequires
* Tue Apr 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.1-1
- Initial runc package for PhotonOS.
