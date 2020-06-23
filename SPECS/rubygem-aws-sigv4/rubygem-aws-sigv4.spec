%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sigv4

Name: rubygem-aws-sigv4
Version:        1.2.2
Release:        1%{?dist}
Summary:        Amazon Web Services Signature Version 4 signing library.
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sigv4-%{version}.gem
%define sha1    aws-sigv4=46bf7f608afeea94c18c17aa460a39b7deef634d
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
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.2-1
-   Automatic Version Bump
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.3-1
-   Initial build
