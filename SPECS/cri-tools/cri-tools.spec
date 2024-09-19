%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.21.0
Release:        18%{?dist}
License:        Apache License Version 2.0
URL:            https://github.com/kubernetes-incubator/cri-tools/archive/%{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}.tar.gz=a307f5526fb8b7b23a1635b168a8f3b9b9b4bd6ccb94d461dc5af2065e6d1be527dadcb1c86e04808b244d0851a4901ee78a0263f58cf673f6ca503621d5eb61

BuildRequires:  go
BuildRequires:  git

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%autosetup -Sgit -p1 -n %{name}-%{version}

%build

%install
make install BUILD_BIN_PATH=%{buildroot}%{_bindir} BUILD_PATH=%{buildroot} %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%check
%if 0%{?with_check}
make test-e2e %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_bindir}/crictl
%exclude %{_bindir}/critest

%changelog
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.21.0-18
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.21.0-17
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.21.0-16
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.21.0-15
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-14
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-13
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-12
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-11
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-10
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-9
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-8
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-6
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-5
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-4
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-3
- Bump up version to compile with new go
* Mon May 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-2
- Bump up version to compile with new go
* Fri May 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.21.0-1
- Upgrade to v1.21.0 & fix spec
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.19.0-9
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.19.0-8
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.19.0-7
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.19.0-6
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.19.0-5
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.19.0-4
- Bump up version to compile with new go
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
