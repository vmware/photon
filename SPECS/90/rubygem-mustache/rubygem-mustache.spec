%global build_if %{photon_subrelease} <= 90
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mustache

Name: rubygem-mustache
Version:        1.1.1
Release:        5.1.1%{?dist}
Summary:        A framework-agnostic way to render logic-free views
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires: ruby

%description
Mustache is a replacement for your views. Instead of views consisting of
ERB or HAML with random helpers and arbitrary logic, your views are broken
into two parts: a Ruby class and an HTML template

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.1.1-5.1.1
- Adjusted to build for subrelease 90
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.1-5.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.1-5
- Spec bump with ruby upgrade
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.1-4
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.1-3
- Release bump for SRP compliance
* Thu Dec 08 2022 Shivani Agarwal <shivania2@vmware.com> 1.1.1-2
- Bump version to build with new Ruby
* Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.1.1-1
- Initial build
