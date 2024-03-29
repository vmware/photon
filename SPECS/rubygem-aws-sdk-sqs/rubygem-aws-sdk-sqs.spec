%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-sqs

Name: rubygem-aws-sdk-sqs
Version:        1.52.0
Release:        1%{?dist}
Summary:        Official AWS Ruby gem for Amazon Simple Queue Service (Amazon SQS).
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sdk-sqs-%{version}.gem
%define sha512    aws-sdk-sqs=db747e42102a383d37c07a7d77f7ea600ec33e86c99cf817bff85a9271a1329385ae8f9f23ce9768f3712196b6d16184d2922f4d25bd7f8f319882011b54b657
BuildRequires:  ruby

Requires: rubygem-aws-sdk-core >= 3
Requires: rubygem-aws-sigv4 >= 1.0

%description
Official AWS Ruby gem for Amazon Simple Queue Service (Amazon SQS).
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
