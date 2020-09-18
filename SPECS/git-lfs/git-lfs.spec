%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
Summary:     Git extension for versioning large files
Name:        git-lfs
Version:     2.12.0
Release:     1%{?dist}
URL:         https://github.com/git-lfs/git-lfs/archive/v%{version}.tar.gz
Source0:     %{name}-%{version}.tar.gz
License:     MIT
Group:       System Environment/Programming
%define sha1 %{name}=fa48d4e536f7d931efb78c5cb3c094746ad83d4a
Vendor:      VMware, Inc.
Distribution:  Photon
BuildRequires: go
BuildRequires: which
BuildRequires: rubygem-ronn
BuildRequires: tar
BuildRequires: git
Requires: git

%description
Git LFS is a command line extension and specification for managing large files with Git

%prep
%setup -q

%build
make %{?_smp_mflags}
export PATH=$PATH:%{gemdir}/bin
make man

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
* Fri Sep 18 2020 Him Kalyan Bordoloi <bordoloih@vmware.com>  2.12.0-1
- Initial release.
