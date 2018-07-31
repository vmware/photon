%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-sqs

Name: rubygem-aws-sdk-sqs
Version:        1.4.0
Release:        1%{?dist}
Summary:        Official AWS Ruby gem for Amazon Simple Queue Service (Amazon SQS).
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sdk-sqs-%{version}.gem
%define sha1    aws-sdk-sqs=7d8283aacd983e7f47518164181e4cda8b519eba
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
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
