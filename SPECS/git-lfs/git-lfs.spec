%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
Summary:       Git extension for versioning large files
Name:          git-lfs
Version:       3.1.4
Release:       1%{?dist}
URL:           https://github.com/git-lfs/git-lfs/archive/v%{version}.tar.gz
Source0:       %{name}-%{version}.tar.gz
License:       MIT
Group:         System Environment/Programming
%define sha512 %{name}=ff62e19532ec09d71e241ffb9b6a0ed91a76cbe1fe32a88a6e3679e15cf97b09bcfdb5fc1aa0c1a9984bc888c88be87940bd7044d68102eadf93cb68dc5e9c1c
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
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.1.4-1
-   Automatic Version Bump
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.13.3-2
-   Bump up version to compile with new go
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.13.3-1
-   Automatic Version Bump
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.12.0-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.12.0-2
-   Bump up version to compile with new go
*   Fri Sep 18 2020 Him Kalyan Bordoloi <bordoloih@vmware.com>  2.12.0-1
-   Initial release.
