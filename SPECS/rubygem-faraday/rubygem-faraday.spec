%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name faraday

Summary:        HTTP/REST API client library.
Name:           rubygem-faraday
Version:        2.14.1
Release:        3%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-faraday-net_http

Requires: ruby
Requires: rubygem-faraday-net_http

%description
HTTP/REST API client library.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.14.1-3
- Extended to build for subrelease 91 and above
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.14.1-2
- bump version with ruby upgrade
* Thu Feb 12 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.14.1-1
- Fix CVE-2026-25765, upgrade to 2.14.1
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.12.2-2
- Spec bump with ruby upgrade
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.12.2-1
- Initial version.
