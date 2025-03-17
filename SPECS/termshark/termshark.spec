%define network_required 1
%define gopath_comp_termshark github.com/gcla/termshark

Summary:        A terminal user-interface for tshark, inspired by Wireshark
Name:           termshark
Version:        2.4.0
Release:        19%{?dist}
URL:            https://github.com/gcla/%{name}/releases/tag/v%{version}.tar.gz
Source0:        https://github.com/gcla/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
BuildRequires:  wireshark-devel
BuildRequires:  libpcap-devel
Requires:       wireshark
Requires:       libpcap

%global debug_package %{nil}

%description
Termshark is the terminal user-interface tor Tshark, a source network protocol analyzer.
TShark doesn't have an interactive terminal user interface though, and this is where
Termshark comes in. Termshark is basically the futuristic terminal version of Wireshark.

%prep
# Using autosetup is not feasible
%setup -q -c -n %{name}-%{version}

mkdir -p "$(dirname src/%{gopath_comp_termshark})"
mv %{name}-%{version} src/%{gopath_comp_termshark}

%build
export GO111MODULE=auto
export GOPATH="${PWD}"
pushd src/%{gopath_comp_termshark}
go build -v ./cmd/...
popd

%install
pushd src/%{gopath_comp_termshark}
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} termshark
popd

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.4.0-19
- Fix go input dependencies which have Capital letters in name.
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.4.0-18
- Release bump for network_required packages
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 2.4.0-17
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.4.0-16
- Bump version as a part of go upgrade
* Tue Sep 03 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.4.0-15
- Version bump up to consume wireshark v4.2.7
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 2.4.0-14
- Simplify build scripts
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.4.0-13
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.4.0-12
- Bump version as a part of go upgrade
* Mon Apr 01 2024 Anmol Jain <anmol.jain@broadcom.com> 2.4.0-11
- Bump version as a part of wireshark upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 2.4.0-10
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-9
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-8
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-7
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-6
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-5
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-4
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.0-3
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.4.0-2
- Bump up version to compile with new go
* Tue Nov 1 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.0-1
- Automatic Version Bump
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-2
- Bump up version to compile with new go
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 2.3.0-1
- Version bump.
* Thu May 06 2021 Susant Sahani <ssahani@vmware.com> 2.2.0-1
- Initial rpm release.
