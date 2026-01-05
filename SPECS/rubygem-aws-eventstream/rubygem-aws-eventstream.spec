%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-eventstream

Name: rubygem-aws-eventstream
Version:        1.3.2
Release:        1%{?dist}
Summary:        Amazon Web Services event stream library.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-eventstream-%{version}.gem
%define sha512  aws-eventstream=1400e5c7a546c17a7707c722aaee90ba7b726ecc5423b76a220e3e9ac1636ea095d33eda0697b31c340d5c20e3e51bd68e263cc10b45a62913245e296da1a1b8
BuildRequires:  ruby

%description
Amazon Web Services event stream library.
Decodes and encodes binary stream under
`vnd.amazon.event-stream` content-type

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jan 05 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.2-1
-   Bump version to 1.3.2 to be compatible with rubygem-aws-sdk-core upgrade
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
-   Automatic Version Bump
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
