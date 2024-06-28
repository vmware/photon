%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.22.0
Release:        11%{?dist}
License:        Apache License Version 2.0
URL:            https://github.com/kubernetes-incubator/cri-tools
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/kubernetes-incubator/%{name}/releases/tag/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}.tar.gz=4a2751ebe0b1ed7cb739a71230272ace0cbddc516abba39c6bf07d5e2648bd60e2139935b77a5388028887915162c957f652ea05434ff7865256721d10f863df

BuildRequires:  go

Requires: calico-cni

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%autosetup -p1

%build
export GO111MODULE=on
export GOFLAGS="-mod=vendor"
# BUILDTAGS can be removed after cri-tools >= v1.24.1
# https://github.com/kubernetes-sigs/cri-tools/pull/931
export BUILDTAGS="selinux seccomp"

%make_build VERSION="%{version}-%{release}"

%install
mkdir -p %{buildroot}%{_bindir}
mv build/bin/crictl %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}/*

%check
%make_build test-e2e

%files
%defattr(-,root,root)
%{_bindir}/crictl

%changelog
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-11
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-10
- Bump up version to compile with new go
* Mon Sep 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.22.0-9
- Add calico-cni to requires
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-8
- Bump up version to compile with new go
* Mon Jul 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.0-7
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
