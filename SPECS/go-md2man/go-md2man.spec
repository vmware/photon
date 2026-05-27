%global build_if %{photon_subrelease} >= 91

Summary:        Converts markdown into roff (man pages)
Name:           go-md2man
Version:        2.0.7
Release:        1%{?dist}
URL:            https://github.com/cpuguy83/go-md2man
Source0:        https://github.com/cpuguy83/go-md2man/archive/%{name}-%{version}.tar.gz
Source2:        %{name}-%{version}-vendor.tar.gz

Source1: license.txt
%include %{SOURCE1}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go >= 1.11

%description
Converts markdown into roff (man pages).

%prep
%autosetup -a 2

%build
go build -mod=vendor -o bin/go-md2man .

%install
install -v -m755 -D -t %{buildroot}%{_bindir} bin/go-md2man
install -v -m644 -D -t %{buildroot}%{_docdir}/licenses/%{name} LICENSE.md

%files
%defattr(-,root,root)
%{_bindir}/go-md2man
%{_docdir}/licenses/%{name}

%changelog
* Fri May 22 2026 Mukul Sikka <mukul.sikka@broadcom.com> 2.0.7-1
- Upgrade to v2.0.7
* Sat Jul 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.2-14
- Bump version as a part of go upgrade
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.0.2-13
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.0.2-12
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.0.2-11
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.0.2-10
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 2.0.2-9
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.2-8
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.2-7
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.2-6
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.2-5
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.2-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.2-3
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.2-2
- Bump up version to compile with new go
* Wed Nov 30 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.1-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.1-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.1-2
- Bump up version to compile with new go
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.1-1
- Automatic Version Bump
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.0-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.0.0-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.0-2
- Bump up version to compile with new go
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.0-1
- Initial packaging for go-md2man for containerd
