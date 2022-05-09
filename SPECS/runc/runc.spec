%define debug_package %{nil}
%define __os_install_post %{nil}

%define RUNC_COMMIT_SHORT f46b6ba
# use major.minor.patch-rcX
%define RUNC_VERSION 1.0.3
%define RUNC_GITTAG v%{RUNC_VERSION}
%define gopath_comp github.com/opencontainers/runc

Summary:        CLI tool for spawning and running containers per OCI spec.
Name:           runc
Version:        1.0.3
Release:        3%{?dist}
License:        ASL 2.0
URL:            https://runc.io
Group:          Virtualization/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/opencontainers/runc/archive/runc-%{version}.tar.gz
%define sha512  %{name}=64a1894c2b4ed5a68b185e88548fc9fbbd01d8a9495feed59fb196aa06763d64cfb71ca6cbc09d1defa26a0d94ad58626296585741f23df2e290147ba6c4c26e

BuildRequires:  go
BuildRequires:  which
BuildRequires:  go-md2man
BuildRequires:  pkg-config
BuildRequires:  libseccomp >= 2.4.0
BuildRequires:  libseccomp-devel

Requires:   libseccomp >= 2.4.0

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
export GO111MODULE=auto
cd src/%{gopath_comp}
# Use the format of `git describe --long` as COMMIT
make %{?_smp_mflags} GIT_BRANCH=%{RUNC_GITTAG} COMMIT=%{RUNC_GITTAG}-0-g%{RUNC_COMMIT_SHORT} BUILDTAGS='seccomp apparmor' EXTRA_LDFLAGS=-w runc man

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
*   Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-3
-   Bump up version to compile with new go
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-2
-   Bump up version to compile with new go
*   Fri Feb 25 2022 Bo Gan <ganb@vmware.com> 1.0.3-1
-   Update to 1.0.3
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-11
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-10
-   Bump up version to compile with new go
* Mon Dec 13 2021 Nitesh Kumar <kunitesh@vmware.com> 1.0.0.rc93-9
- Fix for CVE-2021-43784.
* Thu Nov 25 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.0.0.rc93-8
- Depend on libseccomp >= 2.4.0
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-7
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-6
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0.rc93-5
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-4
- Bump up version to compile with new go
* Tue May 18 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0.rc93-3
- Bump up version to compile with new go
* Fri May 14 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-2
- Fix for CVE-2021-30465
* Wed May 05 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-1
- Bump up version to 1.0.0-rc93 for containerd
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.0.0.rc10-3
- Bump up version to compile with new go
* Tue Dec 1 2020 HarinadhD <hdommaraju@vmware.com> 1.0.0.rc10-2
- Bump up version to compile with new go
* Fri Nov 20 2020 Ankit Jain <ankitja@vmware.com> 1.0.0.rc10-1
- Updated to 1.0.0.rc10
* Wed Jun 03 2020 Harinadh D <hdommaraju@vmware.com> 1.0.0.rc9-3
- Fix CVE-2019-19921
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.0.0.rc9-2
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 1.0.0.rc9-1
- Bump up version to 1.0.0-rc9 for containerd
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.0.0.rc8-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.0.0.rc8-2
- Bump up version to compile with new go
* Thu Jun 13 2019 Tapas Kundu <tkundu@vmware.com> 1.0.0.rc8-1
- Update to release 1.0.0-rc8
* Mon Feb 11 2019 Bo Gan <ganb@vmware.com> 0.1.1-3
- Fix CVE-2019-5736
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.1-2
- Add iptables-devel to BuildRequires
* Tue Apr 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.1-1
- Initial runc package for PhotonOS.
