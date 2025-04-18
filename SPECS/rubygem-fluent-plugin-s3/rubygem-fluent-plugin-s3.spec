%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-s3

Name: rubygem-fluent-plugin-s3
Version:        1.7.2
Release:        3%{?dist}
Summary:        Amazon S3 output plugin for Fluentd event collector.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/fluent-plugin-s3-%{version}.gem
%define sha512 %{gem_name}=3983c451a805e42e0b8329ee4b66ab65eb2bde41cc373de1e3f47e4908d0dc2b92b43901436ccc4174fff1b216461d6afdfb6e04dfa8e38036bb977ce5726e74

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-aws-sdk-s3
BuildRequires: rubygem-fluentd
BuildRequires: rubygem-aws-sdk-sqs

Requires: ruby
Requires: rubygem-aws-sdk-s3 >= 1.0
Requires: rubygem-aws-sdk-s3 >= 1.0
Requires: rubygem-fluentd >= 0.14.2
Requires: rubygem-fluentd < 2.0.0
Requires: rubygem-aws-sdk-sqs >= 1.0

%description
Amazon S3 output plugin for Fluentd event collector.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.2-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.2-2
- Bump Version to build with new ruby
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.2-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Tue Nov 27 2018 Sujay G <gsujay@vmware.com> 1.1.6-2
- Added %check section
* Mon Sep 17 2018 srinidhira0 <srinidhir@vmware.com> 1.1.6-1
- Update to version 1.1.6
* Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.4-1
- Initial build
