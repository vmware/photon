%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.21.0
Release:        15%{?dist}
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
* Mon Jun 24 2024 Mukul Sikka <msikka@vmware.com> 1.21.0-15
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-14
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-13
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-12
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-11
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-10
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-9
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.21.0-8
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-7
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-6
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-5
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-4
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-3
- Bump up version to compile with new go
* Mon May 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.21.0-2
- Bump up version to compile with new go
* Fri May 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.21.0-1
- Upgrade to v1.21.0 & fix spec
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.0-12
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.0-11
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.0-10
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.0-9
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.0-8
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.17.0-7
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.0-6
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.17.0-5
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.17.0-4
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.17.0-3
- Bump up version to compile with new go
* Wed Apr 22 2020 Harinadh D <hdommaraju@vmware.com> 1.17.0-2
- Bump up version to compile with go 1.13.3-2
* Wed Apr 15 2020 Ashwin H <ashwinh@vmware.com> 1.17.0-1
- Update to 1.17.0
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.11.1-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.11.1-2
- Bump up version to compile with new go
* Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
- Initial build added for Photon.
