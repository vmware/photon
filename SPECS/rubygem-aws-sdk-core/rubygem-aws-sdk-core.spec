%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-core

Name: rubygem-aws-sdk-core
Version:        3.166.0
Release:        3%{?dist}
Summary:        Provides API clients for AWS.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sdk-core-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-aws-eventstream
BuildRequires: rubygem-aws-sigv4
BuildRequires: rubygem-aws-partitions
BuildRequires: rubygem-jmespath

Requires: ruby
Requires: rubygem-aws-eventstream >= 1.0
Requires: rubygem-aws-partitions >= 1.0
Requires: rubygem-aws-sigv4 >= 1.0
Requires: rubygem-jmespath >= 1.0

%description
Provides API clients for AWS. This gem is part of the official AWS SDK for Ruby..

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
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.166.0-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.166.0-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.166.0-1
- Automatic Version Bump
* Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.109.0-1
- Automatic Version Bump
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.108.0-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.107.0-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.105.0-1
- Automatic Version Bump
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 3.27.0-1
- Update to version 3.27.0
* Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 3.22.1-1
- Initial build
