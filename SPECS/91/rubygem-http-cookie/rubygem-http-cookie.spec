%global build_if %{photon_subrelease} <= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-cookie

Name: rubygem-http-cookie
Version:        1.0.8
Release:        1.1%{?dist}
Summary:        HTTP::Cookie is a Ruby library to handle HTTP Cookies based on RFC 6265.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-domain_name

Requires: rubygem-domain_name >= 0.5.0, rubygem-domain_name < 1.0.0
Requires: ruby

BuildArch: noarch

%description
HTTP::Cookie is a Ruby library to handle HTTP Cookies based on RFC 6265. It has with
security, standards compliance and compatibility in mind, to behave just the same as
today's major web browsers. It has builtin support for the legacy cookies.txt and the
latest cookies.sqlite formats of Mozilla Firefox, and its modular API makes it easy
to add support for a new backend store.

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
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.8-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.8-1
- Upgrade to 1.0.8
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0.5-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.5-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.5-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.3-2
- Rebuilt using ruby-2.7.1
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.0.3-1
- Initial build
