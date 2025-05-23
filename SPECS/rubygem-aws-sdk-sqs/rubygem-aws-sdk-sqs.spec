%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-sqs

Name: rubygem-aws-sdk-sqs
Version:        1.70.0
Release:        2%{?dist}
Summary:        Official AWS Ruby gem for Amazon Simple Queue Service (Amazon SQS).
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/aws-sdk-sqs-%{version}.gem
%define sha512 %{gem_name}=41b6d077927d0ab360a3ddd47751d991357146ecb4b3ea77c2cadffeff657e52526e7ced538110d760f035ef581c6a9f5339690a4ade919813e2cf9c3ae807fa

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-aws-sdk-core
BuildRequires: rubygem-aws-sigv4

Requires: ruby
Requires: rubygem-aws-sdk-core >= 3
Requires: rubygem-aws-sigv4 >= 1.0

%description
Official AWS Ruby gem for Amazon Simple Queue Service (Amazon SQS).
This gem is part of the AWS SDK for Ruby.

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
*   Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.70.0-2
-   Build gems properly
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.70.0-1
-   Update to version 1.70.0
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.52.0-1
-   Automatic Version Bump
*   Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.34.0-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.33.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.32.0-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.6.0-1
-   Update to version 1.6.0
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
