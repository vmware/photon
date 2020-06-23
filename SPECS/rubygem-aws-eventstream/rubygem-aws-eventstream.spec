%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-eventstream

Name: rubygem-aws-eventstream
Version:        1.1.0
Release:        1%{?dist}
Summary:        Amazon Web Services event stream library.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-eventstream-%{version}.gem
%define sha1    aws-eventstream=016390c0e910f534f4d5a4bceda739cd71ff418c
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
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
-   Automatic Version Bump
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
