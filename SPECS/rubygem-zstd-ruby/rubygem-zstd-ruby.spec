%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name zstd-ruby

Name: rubygem-zstd-ruby
Version:        1.5.7.1
Release:        2%{?dist}
Summary:        Ruby binding for zstd compression algorithm
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/zstd-ruby/versions/%{version}
Source0:        https://rubygems.org/downloads/zstd-ruby-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: gcc
BuildRequires: zstd-devel

Requires: ruby
Requires: zstd

%description
Ruby binding for zstd(Zstandard - Fast real-time compression algorithm).
See https://github.com/facebook/zstd

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.5.7.1-2
- Extended to build for subrelease 91 and above
* Tue Jan 27 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.5.7.1-1
- Initial build for fluentd dependency
