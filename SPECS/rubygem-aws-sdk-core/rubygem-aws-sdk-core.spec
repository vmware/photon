%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-core

Name: rubygem-aws-sdk-core
Version:        3.108.0
Release:        1%{?dist}
Summary:        Provides API clients for AWS.
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sdk-core-%{version}.gem
%define sha1    aws-sdk-core=8559d9dd03d1e23ffc6bdcc0b5ea558717f5c6a8
BuildRequires:  ruby

Requires: rubygem-aws-eventstream >= 1.0
Requires: rubygem-aws-partitions >= 1.0
Requires: rubygem-aws-sigv4 >= 1.0
Requires: rubygem-jmespath >= 1.0

%description
Provides API clients for AWS. This gem is part of the official AWS SDK for Ruby..

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
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
