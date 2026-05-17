%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name faraday-follow_redirects

Name: rubygem-faraday-follow_redirects
Version:        0.5.0
Release:        2%{?dist}
Summary:        Faraday middleware for following redirects
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/faraday-follow_redirects/versions/%{version}
Source0:        https://rubygems.org/downloads/faraday-follow_redirects-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-faraday

Requires: ruby
Requires: rubygem-faraday >= 1.0

%description
Faraday 1.x and 2.x compatible extraction of FaradayMiddleware::FollowRedirects.
This middleware follows HTTP redirects for Faraday connections.

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.5.0-2
- Extended to build for subrelease 91 and above
* Tue Jan 27 2026 Mukul Sikka <mukul.sikka@broadcom.com> 0.5.0-1
- Initial build for google-apis-core dependency
