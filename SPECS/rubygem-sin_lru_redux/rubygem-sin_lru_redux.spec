%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name sin_lru_redux

Name: rubygem-sin_lru_redux
Version:        2.5.2
Release:        2%{?dist}
Summary:        Efficient and thread-safe LRU cache
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/sin_lru_redux/versions/%{version}
Source0:        https://rubygems.org/downloads/sin_lru_redux-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Efficient and thread-safe LRU cache implementation for Ruby.
A high-performance LRU (Least Recently Used) cache with thread-safety.

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.5.2-2
- Extended to build for subrelease 91 and above
* Tue Jan 27 2026 Mukul Sikka <mukul.sikka@broadcom.com> 2.5.2-1
- Initial build for fluent-plugin-kubernetes_metadata_filter dependency
