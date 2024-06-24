%define debug_package %{nil}
%define __os_install_post %{nil}
%define gopath_comp github.com/%{name}/%{name}

Summary:        Containerd
Name:           containerd
Version:        1.6.8
Release:        11%{?dist}
License:        ASL 2.0
URL:            https://containerd.io/docs
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/containerd/archive/containerd-%{version}.tar.gz
%define sha512 %{name}=c204c028cdfd76537d1da01c66526fc85b29b02d2412569bb9b265375603614b037356c61846025a72281398f0f46df326a5ea3df97f57901cce85f2f728f0ba

# Must be in sync with package version
%define CONTAINERD_GITCOMMIT 9cd3357b7fd7218e4aec3eae239db1f68a5a6ec6

Source1: %{name}-config.toml
Source2: disable-%{name}-by-default.preset

Patch0: %{name}-service.patch
Patch1: build-bin-gen-manpages-instead-of-using-go-run.patch
Patch2: CVE-2022-23471.patch
Patch3: CVE-2023-25153.patch
Patch4: CVE-2023-25173.patch

BuildRequires:  btrfs-progs
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
# Upstream is unhappy with 1.14. 1.13 or 1.15+ is OK
BuildRequires:  go >= 1.16
BuildRequires:  go-md2man
BuildRequires:  systemd-devel

Requires:       libseccomp
Requires:       systemd
# containerd 1.4.5 and above allow to use runc 1.0.0-rc94 and above.
# refer to v1.4.5/RUNC.md
Requires:       runc

%description
Containerd is an open source project. It is available as a daemon for Linux,
which manages the complete container lifecycle of its host system.

%package        extras
Summary:        Extra binaries for containerd
Group:          Applications/File
Requires:       %{name} = %{version}-%{release}

%description    extras
Extra binaries for containerd

%package        doc
Summary:        containerd
Requires:       %{name} = %{version}-%{release}

%description    doc
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
* Mon Jun 24 2024 Mukul Sikka <msikka@vmware.com> 1.6.8-11
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.8-10
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.8-9
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.8-8
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.8-7
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.8-6
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.8-5
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.8-4
- Bump up version to compile with new go
* Mon Mar 06 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.6.8-3
- Fix CVE-2023-25153 & CVE-2023-25173
* Tue Feb 14 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.6.8-2
- Fix CVE-2022-23471
* Mon Jan 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.6.8-1
- Upgrade to v1.6.8
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.13-8
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.13-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.13-6
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.13-5
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.13-4
- Bump up version to compile with new go
* Sun Jul 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.13-3
- Use correct git commit id
* Tue Jun 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.13-2
- Bump up version to compile with new go
* Fri Jun 03 2022 Bo Gan <ganb@vmware.com> 1.4.13-1
- Upgrade to 1.4.13
- Fix CVE-2022-31030 with ExecSync API
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.12-2
- Bump up version to compile with new go
* Fri Feb 25 2022 Bo Gan <ganb@vmware.com> 1.4.12-1
- Update to 1.4.12 and fix CVE-2022-23648
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.4-10
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.4-9
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-8
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-7
- Bump up version to compile with new go
* Fri Oct 01 2021 Bo Gan <ganb@vmware.com> 1.4.4-6
- Fix CVE-2021-41103
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.4-5
- Bump up version to compile with new go
* Tue Jul 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-4
- Bump up version to compile with new go.
* Fri Jul 16 2021 Bo Gan <ganb@vmware.com> 1.4.4-3
- Fix CVE-2021-32760
* Tue May 18 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.4-2
- Bump up version to compile with new go
* Wed May 05 2021 Bo Gan <ganb@vmware.com> 1.4.4-1
- Update to 1.4.4
* Mon Mar 22 2021 Ankit Jain <ankitja@vmware.com> 1.3.10-1
- Update to 1.3.10 to fix CVE-2021-21334
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.3.9-3
- Bump up version to compile with new go
* Tue Dec 1 2020 HarinadhD <hdommaraju@vmware.com> 1.3.9-2
- Bump up version to compile with new go
* Mon Nov 30 2020 Bo Gan <ganb@vmware.com> 1.3.9-1
- Update to 1.3.9 for upstream fix of CVE-2020-15257
* Fri Nov 20 2020 Ankit Jain <ankitja@vmware.com> 1.3.7-1
- Update to 1.3.7 to fix CVE-2020-15257
* Fri Oct 16 2020 Ashwin H <ashwinh@vmware.com> 1.2.14-1
- Update to 1.2.14 to fix CVE-2020-15157
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.10-3
- enable critical restart
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.10-2
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 1.2.10-1
- Bump up version to 1.2.10 and cleanups
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.8-2
- Bump up version to compile with go 1.13.3
* Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
- Initial version of containerd spec.
