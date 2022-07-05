%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.21.0
Release:        3%{?dist}
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
