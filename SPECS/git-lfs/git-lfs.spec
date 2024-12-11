%define network_required 1
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
Summary:       Git extension for versioning large files
Name:          git-lfs
Version:       3.2.0
Release:       13%{?dist}
URL:           https://github.com/git-lfs/git-lfs/archive/v%{version}.tar.gz
Source0:       https://github.com/git-lfs/git-lfs/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=c2ba8cecd5b3519a032f446b0c3043352f37f3c67ff3c2304a38beb176f0ae8efd1deaeb8bd54a35d7dd7dcd988da67249c896dffd83fc293b165a3e6bb02d66

Source1: license.txt
%include %{SOURCE1}
Group:         System Environment/Programming
Vendor:        VMware, Inc.
Distribution:  Photon
BuildRequires: go
BuildRequires: which
BuildRequires: rubygem-ronn
BuildRequires: tar
BuildRequires: git
Requires:      git

%description
Git LFS is a command line extension and specification for managing large files with Git

%prep
%autosetup

%build
make %{?_smp_mflags}
export PATH=$PATH:%{gemdir}/bin
make man %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -D bin/git-lfs %{buildroot}%{_bindir}/git-lfs
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
install -D man/man1/* %{buildroot}%{_mandir}/man1
install -D man/man5/* %{buildroot}%{_mandir}/man5

%post
git lfs install --system

%preun
git lfs uninstall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.md README.md
%{_bindir}/git-lfs
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.2.0-13
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.2.0-12
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.2.0-11
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 3.2.0-10
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 3.2.0-9
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-8
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-7
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-6
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-5
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-3
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-2
- Bump up version to compile with new go
* Wed Nov 30 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 3.1.4-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.1.4-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.1.4-2
- Bump up version to compile with new go
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.1.4-1
- Automatic Version Bump
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.13.3-2
- Bump up version to compile with new go
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.13.3-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.12.0-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.12.0-2
- Bump up version to compile with new go
* Fri Sep 18 2020 Him Kalyan Bordoloi <bordoloih@vmware.com>  2.12.0-1
- Initial release.
