%define debug_package %{nil}
%define __os_install_post %{nil}

# use major.minor.patch-rcX
%define RUNC_VERSION 1.1.12
%define RUNC_BRANCH  v%{RUNC_VERSION}

%define gopath_comp  github.com/opencontainers/runc

Summary:             CLI tool for spawning and running containers per OCI spec.
Name:                runc
Version:             1.1.12
Release:             2%{?dist}
License:             ASL 2.0
URL:                 https://runc.io
Group:               Virtualization/Libraries
Vendor:              VMware, Inc.
Distribution:        Photon

Source0: https://github.com/opencontainers/runc/archive/runc-%{version}.tar.gz
%define sha512 %{name}=92e8ac54a77d7ebcc76b5a9cc08d9a064211f12e9d26f064070cc203a5afb11c3af28d8f556f297513f797a2933d50bf10a8f22e307724041d66aa8c5ca1d9d3

BuildRequires: go
BuildRequires: which
BuildRequires: go-md2man
BuildRequires: pkg-config
BuildRequires: libseccomp
BuildRequires: libseccomp-devel

%description
runC is a CLI tool for spawning and running containers according to the OCI specification.
Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%package             doc
Summary:             Documentation for runc
Requires:            %{name} = %{version}-%{release}

%description doc
Documentation for runc

%prep
%autosetup -p1 -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{version} src/%{gopath_comp}

%build
export GOPATH="$PWD"
cd src/%{gopath_comp}

%make_build \
        GIT_BRANCH=%{RUNC_BRANCH} \
        BUILDTAGS='seccomp selinux apparmor' \
        EXTRA_LDFLAGS=-w %{name} man

%install
cd src/%{gopath_comp}
%make_install %{?_smp_flags} \
        DESTDIR=%{buildroot} PREFIX=%{_prefix} \
        BINDIR=%{_bindir} \
        install-bash install-man

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}

%files doc
%defattr(-,root,root)
%{_mandir}/man8/*

%changelog
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.1.12-2
- Bump version as a part of go upgrade
* Tue Feb 06 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.1.12-1
- Version upgrade to v1.1.12 to fix CVE-2024-21626
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-12
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-11
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-10
- Bump up version to compile with new go
* Mon Jul 10 2023 Nitesh Kumar <kunitesh@vmware.com> 1.1.4-9
- Patched for CVE-2023-25809
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-8
- Bump up version to compile with new go
* Tue May 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-7
- Fix CVE-2023-27561
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-6
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-5
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.4-4
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.4-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.4-2
- Bump up version to compile with new go
* Tue Oct 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.4-1
- Upgrade to v1.1.4.
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.1-5
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.1-4
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.1-3
- Bump up version to compile with new go
* Mon May 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.1-2
- Bump up version to compile with new go
* Sat May 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.1-1
- Upgrade to v1.1.1 & enable selinux in BUILDTAGS
* Fri Feb 25 2022 Bo Gan <ganb@vmware.com> 1.0.3-4
- Fix build commit hash and tag
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-3
- Bump up version to compile with new go
* Fri Feb 11 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-2
- Bump up version to compile with new go
* Mon Dec 13 2021 Nitesh Kumar <kunitesh@vmware.com> 1.0.3-1
- Version upgrade to fix CVE-2021-43784.
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-5
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-4
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-3
- Bump up version to compile with new go
* Fri May 14 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-2
- Fix for CVE-2021-30465
* Wed May 05 2021 Bo Gan <ganb@vmware.com> 1.0.0.rc93-1
- Bump up version to 1.0.0-rc93
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0.rc92-4
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
