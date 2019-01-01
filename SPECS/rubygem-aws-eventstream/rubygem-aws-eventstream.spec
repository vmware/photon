%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-eventstream

Name: rubygem-aws-eventstream
Version:        1.0.1
Release:        2%{?dist}
Summary:        Amazon Web Services event stream library.
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-eventstream-%{version}.gem
%define sha1    aws-eventstream=bffa80739c9f404cd67cdcf35aa9f17ffdca7ebc
BuildRequires:  ruby

%description
Amazon Web Services event stream library.
Decodes and encodes binary stream under
`vnd.amazon.event-stream` content-type

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.0.1-2
-   Increment the release version as part of ruby upgrade
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
