%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name highline

Name:           rubygem-highline
Version:        3.1.2
Release:        3%{?dist}
Summary:        A high-level IO library that provides validation, type conversion, and more for command-line interfaces
Group:          Applications/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}
Source0:        https://rubygems.org/downloads/highline-%{version}.gem

Source1:        license.txt
%include        %{SOURCE1}

BuildRequires:  ruby-devel

Requires:       ruby

%description
A high-level IO library that provides validation, type conversion, and more for command-line interfaces

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%check
cd %{buildroot}%{gemdir}/gems/highline-%{version}
gem install bundler code_statistics
LANG=en_US.UTF-8  rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.1.2-3
- Extended to build for subrelease 91 and above
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.2-2
- bump version with ruby upgrade
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.2-1
- Upgrade to 3.1.2
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.3-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.0.3-2
- Release bump for SRP compliance
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.3-1
- Automatic Version Bump
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.0.0-1
- Update to version 2.0.0
* Tue Sep 05 2017 Chang Lee <changlee@vmware.com> 1.7.8-4
- Added %check
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.7.8-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.8-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 1.7.8-1
- Initial build
