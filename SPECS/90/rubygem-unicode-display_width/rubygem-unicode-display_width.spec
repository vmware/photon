%global build_if %{photon_subrelease} <= 90
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name unicode-display_width

Summary:        Unicode::DisplayWidth.
Name:           rubygem-unicode-display_width
Version:        3.1.4
Release:        1.1.1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/janlelis/unicode-display_width
Source0:        http://rubygems.org/gems/unicode-display_width-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-unicode-emoji

Requires:       ruby
Requires:       rubygem-unicode-emoji

%description
Determines the monospace display width of a string in Ruby. Implementation based on EastAsianWidth.txt and other data, 100% in Ruby. Other than wcwidth(), which fulfills a similar purpose, it does not rely on the OS vendor to provide an up-to-date method for measuring string width.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%check
cd %{buildroot}%{gemdir}/gems/unicode-display_width-%{version}
gem install yard jeweler rake rspec unicode-emoji
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.1.4-1.1.1
- Adjusted to build for subrelease 90
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-1
- Upgrade to 3.1.4
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.3.0-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.3.0-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
- Automatic Version Bump
* Thu Nov 22 2018 Sujay G <gsujay@vmware.com> 1.4.0-2
- Updated %check
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.4.0-1
- Update to version 1.4.0
* Fri Jun 23 2017 Chang Lee <changlee@vmware.com> 1.1.3-2
- Updated %check
* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.1.3-1
- Initial build
