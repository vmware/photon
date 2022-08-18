%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-core

Name: rubygem-aws-sdk-core
Version:        3.166.0
Release:        1%{?dist}
Summary:        Provides API clients for AWS.
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sdk-core-%{version}.gem
%define sha512    aws-sdk-core=bb06f9e9a06a2e8154485ec560f3b629759c8c144dc1d778d5f0517d9b07756f7cf16c8ce5fd80c2de413e6bdf9ff18c5f8b31ee6cf576cca355656349461dd3
BuildRequires:  ruby

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
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.166.0-1
-   Automatic Version Bump
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
