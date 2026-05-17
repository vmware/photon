%global build_if %{photon_subrelease} <= 90
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name os

Summary:        The OS gem allows for some easy telling if you're on windows or not.
Name:           rubygem-os
Version:        1.1.4
Release:        2.1.1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

%if 0%{?with_check}
BuildRequires: git
%endif

Requires: ruby

%description
The OS gem allows for some easy telling if you’re on windows or not. OS.windows?
as well as some other helper utilities

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%check
cd %{buildroot}%{gemdir}/gems/%{gem_name}-%{version}
[[ $(ruby -r"./lib/os" -e "puts OS.cpu_count") -gt 0 ]] || exit 1
[[ "$(ruby -r"./lib/os" -e "puts OS.bits")" =~ ^(32|64)$ ]] || exit 1

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.1.4-2.1.1
- Adjusted to build for subrelease 90
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.4-2.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.4-2
- Spec bump with ruby upgrade
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.4-1
- Initial version.
