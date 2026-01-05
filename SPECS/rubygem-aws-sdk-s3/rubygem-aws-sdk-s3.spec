%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-s3

Name: rubygem-aws-sdk-s3
Version:        1.209.0
Release:        1%{?dist}
Summary:        Official AWS Ruby gem for Amazon Simple Storage Service (Amazon S3).
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://github.com/aws/aws-sdk-ruby/tree/master/gems/aws-sdk-s3-%{version}.gem
%define sha512  aws-sdk-s3=3de2b949f162a8b44403261bc9bd10b2c5cc47e1c0970d1b152f5580720c9d3ea012bc911d6566442d8cc40e70cea679673c75e27cfdac6b314eeb168c996a05
BuildRequires:  ruby

Requires: rubygem-aws-sdk-core >= 3.21.2
Requires: rubygem-aws-sdk-kms >= 1
Requires: rubygem-aws-sigv4 >= 1.0

%description
Official AWS Ruby gem for Amazon Simple Storage Service (Amazon S3).
This gem is part of the AWS SDK for Ruby.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jan 05 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.209.0-1
-   Upgrade to 1.209.0 to fix CVE-2025-14762
*   Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.82.0-1
-   Automatic Version Bump
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.81.1-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.81.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.79.1-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.19.0-1
-   Update to version 1.19.0
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.17.0-1
-   Initial build
