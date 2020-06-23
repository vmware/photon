%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-s3

Name: rubygem-fluent-plugin-s3
Version:        1.4.0
Release:        1%{?dist}
Summary:        Amazon S3 output plugin for Fluentd event collector.
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluent-plugin-s3-%{version}.gem
%define sha1    fluent-plugin-s3=4e79e5fe29667884e653f3ef2a04a4866cc2f1fc
BuildRequires:  ruby
%if %{with_check}
BuildRequires:  git
%endif

Requires: rubygem-aws-sdk-s3 >= 1.0
Requires: rubygem-aws-sdk-s3 >= 1.0
Requires: rubygem-fluentd >= 0.14.2
Requires: rubygem-fluentd < 2.0.0
Requires: rubygem-aws-sdk-sqs >= 1.0

%description
Amazon S3 output plugin for Fluentd event collector.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/fluent-plugin-s3-%{version}
gem install bundler aws-sdk-s3 aws-sdk-sqs fluentd_regexp_tester test-unit-rr timecop uuidtools
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
-   Automatic Version Bump
*   Tue Nov 27 2018 Sujay G <gsujay@vmware.com> 1.1.6-2
-   Added %check section
*   Mon Sep 17 2018 srinidhira0 <srinidhir@vmware.com> 1.1.6-1
-   Update to version 1.1.6
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.4-1
-   Initial build
