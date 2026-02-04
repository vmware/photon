%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.34.0
Release:        2%{?dist}
URL:            https://github.com/kubernetes-incubator/cri-tools
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/kubernetes-incubator/%{name}/releases/tag/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  go
BuildRequires:  git

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%autosetup -Sgit -p1 -n %{name}-%{version}
# Remove files to handle unintended copyright inclusions
rm vendor/github.com/opencontainers/go-digest/LICENSE.docs
rm vendor/github.com/opencontainers/go-digest/README.md
rm vendor/github.com/opencontainers/go-digest/CONTRIBUTING.md

%build

%install
make install %{?_smp_mflags} \
  BUILD_PATH=%{buildroot} \
  BUILD_BIN_PATH=%{buildroot}%{_bindir} \

%clean
rm -rf %{buildroot}/*

%if 0%{?with_check}
%check
make test-e2e %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_bindir}/crictl
%exclude %{_bindir}/critest

%changelog
* Wed Feb 04 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.34.0-2
- Bump version as a part of go upgrade
* Fri Oct 10 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.34.0-1
- Upgrade to v1.34.0
* Thu Oct 09 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.33.0-1
- Upgrade to v1.33.0
* Fri Jul 25 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.22.0-17
- Remove files to handle unintended copyright inclusions
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.22.0-16
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.22.0-15
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.22.0-14
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.22.0-13
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.22.0-12
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-11
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-10
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-9
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-8
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-7
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-6
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-5
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.22.0-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.22.0-3
- Bump up version to compile with new go
* Tue Jul 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.22.0-2
- Bump up version to compile with new go
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 1.22.0-1
- Automatic Version Bump
* Fri May 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.21.0-3
- Fix spec
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.21.0-2
- Bump up version to compile with new go
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.21.0-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.19.0-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.19.0-2
- Bump up version to compile with new go
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.18.0-1
- Automatic Version Bump
* Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
- Initial build added for Photon.
