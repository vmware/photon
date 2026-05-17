%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-url

Name: rubygem-protocol-url
Version:        0.4.0
Release:        2%{?dist}
Summary:        Provides abstractions for working with URLs
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/protocol-url/versions/%{version}
Source0:        https://rubygems.org/downloads/protocol-url-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Provides abstractions for working with URLs.
Part of the Protocol family of libraries for async I/O.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.4.0-2
- Extended to build for subrelease 91 and above
* Tue Jan 27 2026 Mukul Sikka <mukul.sikka@broadcom.com> 0.4.0-1
- Initial build for async-http dependency
