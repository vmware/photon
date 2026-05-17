%global build_if %{photon_subrelease} <= 90
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo-data

Name: rubygem-tzinfo-data
Version:        1.2025.2
Release:        1.1.1%{?dist}
Summary:        data from the IANA Time Zone database packaged as Ruby modules
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/tzinfo-data-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-tzinfo

Requires: rubygem-tzinfo
Requires: ruby

%description
TZInfo::Data contains data from the IANA Time Zone database packaged as
Ruby modules for use with TZInfo.

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.2025.2-1.1.1
- Adjusted to build for subrelease 90
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2025.2-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2025.2-1
- Upgrade to 1.2025.2
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2022.6-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2022.6-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2022.6-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2020.1-1
- Automatic Version Bump
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2018.5-1
- Initial build
