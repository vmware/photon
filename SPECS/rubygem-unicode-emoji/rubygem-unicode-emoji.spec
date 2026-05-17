%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name unicode-emoji

Summary:        A Ruby gem for working with Unicode Emoji characters
Name:           rubygem-unicode-emoji
Version:        4.2.0
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch: noarch

%description
Unicode Emoji is a Ruby gem that provides a way to handle and manipulate Unicode emoji characters in Ruby.

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.2.0-2
- Extended to build for subrelease 91 and above
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.2.0-1
- Update to version 4.2.0
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.0.4-1
- Initial version.
