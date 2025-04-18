%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name public_suffix

Name:           rubygem-public_suffix
Version:        5.0.4
Release:        2%{?dist}
Summary:        PublicSuffix can parse and decompose a domain name into top level domain, domain and subdomains.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=a9bfce01a5d6c075ed626ea91ea6458b40611b42d18ccb82a6e96586793c570fc934d4268742fd7e44aa73632fada9cda2b63179b018255ad64f6d3a41672c9c

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires: ruby

BuildArch: noarch

%description
PublicSuffix can parse and decompose a domain name into top level domain, domain and subdomains.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0.4-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.0.4-1
- Update to version 5.0.4
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 5.0.0-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.6-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 3.1.1-2
- Built with ruby-2.7.1
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.1.1-1
- Initial build
