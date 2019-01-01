%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sigv4

Name: rubygem-aws-sigv4
Version:        1.0.3
Release:        2%{?dist}
Summary:        Amazon Web Services Signature Version 4 signing library.
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sigv4-%{version}.gem
%define sha1    aws-sigv4=73be50b9a8b4084c246a14ef3689a8c9a3b17b5c
BuildRequires:  ruby

%description
Amazon Web Services Signature Version 4 signing library.
Generates sigv4 signature for HTTP requests.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.0.3-2
-   Increment the release version as part of ruby upgrade
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.3-1
-   Initial build
