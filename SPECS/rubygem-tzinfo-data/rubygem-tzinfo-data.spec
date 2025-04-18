%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo-data

Name:           rubygem-tzinfo-data
Version:        1.2024.1
Release:        2%{?dist}
Summary:        data from the IANA Time Zone database packaged as Ruby modules
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/tzinfo-data-%{version}.gem
%define sha512 %{gem_name}=2839264d4bb07f8df7d7b787ce84dc0d805f61910fcc8cd46b7809b9b62e2d8d320ecdcc2aa72e44103636147f7b095a99ae11ce06b909143dccbe0283f4a68e

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-tzinfo

Requires: rubygem-tzinfo
Requires: ruby

%description
TZInfo::Data contains data from the IANA Time Zone database packaged as
Ruby modules for use with TZInfo.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2024.1-2
-   Build gems properly
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2024.1-1
-   Update to version 1.2024.1
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2022.6-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2022.6-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2020.1-1
- Automatic Version Bump
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2018.5-1
- Initial build
