%define debug_package %{nil}
%define __os_install_post %{nil}

# use major.minor.patch-rcX
%define RUNC_BRANCH  v%{version}
%define gopath_comp  github.com/opencontainers/runc

Summary:             CLI tool for spawning and running containers per OCI spec.
Name:                runc
Version:             1.1.4
Release:             10%{?dist}
License:             ASL 2.0
URL:                 https://runc.io
Group:               Virtualization/Libraries
Vendor:              VMware, Inc.
Distribution:        Photon

Source0: https://github.com/opencontainers/runc/archive/runc-%{version}.tar.gz
%define sha512 %{name}=c8e79ad839964680d29ab56a4de255f91192741951673025da6889c544a232d4d392db2da8005d8e22999a37bfbc9c9fe7f6043b165bc4edc2f2a29261d8a3d6

Patch0:              CVE-2023-27561.patch
Patch1:              CVE-2023-25809.patch

BuildRequires:       go
BuildRequires:       which
BuildRequires:       go-md2man
BuildRequires:       pkg-config
BuildRequires:       libseccomp-devel

Requires:   libseccomp >= 2.4.0

%description
runC is a CLI tool for spawning and running containers according to the OCI specification.
Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%package             doc
Summary:             Documentation for runc
Requires:            %{name} = %{version}-%{release}

%description doc
Documentation for runc

%prep
# Using autosetup is not feasible
%setup -q -c
pushd %{name}-%{version}
%patch0 -p1
%patch1 -p1
popd

mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{version} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
%make_build GIT_BRANCH=%{RUNC_BRANCH} \
            BUILDTAGS='seccomp selinux apparmor' \
            EXTRA_LDFLAGS=-w %{name} man

%install
cd src/%{gopath_comp}
%make_install %{?_smp_mflags} \
        DESTDIR=%{buildroot} PREFIX=%{_prefix} \
        BINDIR=%{_bindir} install-bash install-man

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}

%files doc
%defattr(-,root,root)
%{_mandir}/man8/*

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-10
- Bump up version to compile with new go
* Fri Nov 10 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-9
- Fix CVE-2023-25809
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-8
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-7
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-6
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-5
- Bump up version to compile with new go
* Tue May 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-4
- Fix CVE-2023-27561
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-3
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.4-2
- Bump up version to compile with new go
* Mon Jan 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-1
- Upgrade to v1.1.4
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-6
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-4
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-3
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-2
- Bump up version to compile with new go
* Fri Jun 10 2022 Shivani Agarwal <shivania2@vmware.com> 1.1.3-1
- Upgrde runc to fix CVE-2022-24769, CVE-2022-29162
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-3
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.3-2
- Bump up version to compile with new go
* Fri Feb 25 2022 Bo Gan <ganb@vmware.com> 1.0.3-1
- Update to 1.0.3
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-11
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.0.rc93-10
- Bump up version to compile with new go
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
