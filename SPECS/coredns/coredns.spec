%define network_required 1
%define gopath_comp_coredns github.com/coredns/coredns
%define debug_package %{nil}

# Must be in sync with package version
%define COREDNS_GIT_COMMIT ae2bbc29b

Summary:        CoreDNS
Name:           coredns
Version:        1.11.1
Release:        7%{?dist}
License:        Apache License 2.0
URL:            https://github.com/%{name}/%{name}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/coredns/coredns/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=f8752811e9e7913311f47ae13f35c755ac86ea240572be1c1dabc1712b6c42380c60ac385fa9573c77d6fcf4c144df2bc00574f18e8d7b70da21ed8ae4fb87cd

BuildRequires: go
BuildRequires: git

%description
CoreDNS is a DNS server that chains plugins

%prep -p exit
# Using autosetup is not feasible
%setup -q -c -n %{name}-%{version}

mkdir -p "$(dirname src/%{gopath_comp_coredns})"
mv %{name}-%{version} src/%{gopath_comp_coredns}

%build
export GO111MODULE=auto
export GOPATH="${PWD}"
pushd src/%{gopath_comp_coredns}
%make_build GITCOMMIT=%{COREDNS_GIT_COMMIT}
popd

%install
pushd src/%{gopath_comp_coredns}
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} coredns
popd

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.11.1-7
- Bump version as a part of go upgrade
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 1.11.1-6
- Simplify build scripts, and pass GITCOMMIT to make.
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.11.1-5
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.11.1-4
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.11.1-3
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.11.1-2
- Bump up version to compile with new go
* Fri Nov 03 2023 Nitesh Kumar <kunitesh@vmware.com> 1.11.1-1
- Version upgrade to v1.11.1 to fix following CVE's:
- CVE-2021-28235 and CVE-2023-32082
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.10.1-4
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.10.1-3
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.10.1-2
- Bump up version to compile with new go
* Tue Jul 04 2023 Nitesh Kumar <kunitesh@vmware.com> 1.10.1-1
- Version upgrade to v1.10.1 to fix CVE-2023-0296
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.10.0-5
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.10.0-4
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.10.0-3
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-2
- Bump up version to compile with new go
* Thu Nov 03 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10.0-1
- Version upgrade to v1.10.0
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.3-3
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.3-2
- Bump up version to compile with new go
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.8.3-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.7.1-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.7.1-2
- Bump up version to compile with new go
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.1-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
- Automatic Version Bump
* Sun Sep 22 2019 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-3
- Fix compilation issue (do not compile mholt/caddy).
* Sun Sep 23 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-2
- Fix compilation issue.
- aarch64 support.
* Fri Aug 03 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.2.0-1
- Initial version of coredns 1.2.0.
