%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-sqs

Name: rubygem-aws-sdk-sqs
Version:        1.6.0
Release:        1%{?dist}
Summary:        Official AWS Ruby gem for Amazon Simple Queue Service (Amazon SQS).
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sdk-sqs-%{version}.gem
%define sha1    aws-sdk-sqs=5b729ae9d9ca3298d044dc31aa731df964914f20
BuildRequires:  ruby

Requires: rubygem-aws-sdk-core >= 3
Requires: rubygem-aws-sigv4 >= 1.0

%description
Official AWS Ruby gem for Amazon Simple Queue Service (Amazon SQS).
This gem is part of the AWS SDK for Ruby.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.6.0-1
-   Update to version 1.6.0
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
