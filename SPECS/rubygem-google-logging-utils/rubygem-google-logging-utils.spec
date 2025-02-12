%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-logging-utils

Summary:        Utility classes for logging to Google Cloud Logging
Name:           rubygem-google-logging-utils
Version:        0.1.0
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=023f9111c4df6845cc08e4f8b011bd63d1987862c4bc7ab24d00b1a7e1e6e3ca011d65977b5842224f3988d376548cc0c511487babe29555bd84b1cf9aeb8e11

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Utility classes for logging to Google Cloud Logging

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.1.0-1
- Initial version.
