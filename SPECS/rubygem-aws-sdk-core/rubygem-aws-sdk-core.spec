%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-core

Name: rubygem-aws-sdk-core
Version:        3.109.0
Release:        2%{?dist}
Summary:        Provides API clients for AWS.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/aws-sdk-core-%{version}.gem
%define sha512  aws-sdk-core=cf8e0ca9297665a067be6708d075dedad5cda50a8b666ab77bcee2c22a6dad1c9339ff5cee78e06f3869d60715c8ec4b3fdd0b83c90b0fbf8dc19b3100f5b4e9

BuildRequires:  ruby-devel

Requires: ruby
Requires: rubygem-aws-eventstream >= 1.0
Requires: rubygem-aws-partitions >= 1.0
Requires: rubygem-aws-sigv4 >= 1.0
Requires: rubygem-jmespath >= 1.0

%description
Provides API clients for AWS. This gem is part of the official AWS SDK for Ruby..

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon May 19 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.109.0-2
-   Bump release with rubygem-jmespath upgrade
*   Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.109.0-1
-   Automatic Version Bump
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.108.0-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.107.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.105.0-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 3.27.0-1
-   Update to version 3.27.0
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 3.22.1-1
-   Initial build
