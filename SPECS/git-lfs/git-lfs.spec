%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})

Summary:      Git extension for versioning large files
Name:         git-lfs
Version:      2.12.0
Release:      25%{?dist}
License:      MIT
URL:          https://github.com/git-lfs/git-lfs/archive/v%{version}.tar.gz
Group:        System Environment/Programming
Vendor:       VMware, Inc.
Distribution: Photon

Source0: %{name}-%{version}.tar.gz
%define sha512  %{name}=be143f4008040504357e6e8748e6549bcff08c42340c1cca14b6d617c7a215554c6c3ad8b4c1ce26906bc812ef21c9aa4c8b6f36be2c01a65952c5e075ad81da

BuildRequires: go
BuildRequires: which
BuildRequires: rubygem-ronn
BuildRequires: tar
BuildRequires: git

Requires: git

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
install -D man/*.1 %{buildroot}%{_mandir}/man1
install -D man/*.5 %{buildroot}%{_mandir}/man5

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
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.12.0-25
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.12.0-24
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 2.12.0-23
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.12.0-22
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.12.0-21
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.12.0-20
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 2.12.0-19
- Bump up version to compile with new go
* Wed Feb 01 2023 Nitesh Kumar <kunitesh@vmware.com> 2.12.0-18
- Bump up version as a part of git upgrade to v2.35.6
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-17
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-16
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-15
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-14
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-13
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-12
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-11
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-10
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 2.12.0-9
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 2.12.0-8
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 2.12.0-7
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 2.12.0-6
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 2.12.0-5
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 2.12.0-4
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 2.12.0-3
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 2.12.0-2
- Bump up version to compile with new go
* Fri Sep 18 2020 Him Kalyan Bordoloi <bordoloih@vmware.com>  2.12.0-1
- Initial release.
