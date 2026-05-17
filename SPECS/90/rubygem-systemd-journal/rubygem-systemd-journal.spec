%global build_if %{photon_subrelease} <= 90
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name systemd-journal

Name: rubygem-systemd-journal
Version:        2.1.0
Release:        1.1.1%{?dist}
Summary:        Provides the ability to navigate and read entries from the systemd journal in ruby
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/systemd-journal-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-ffi

Requires: ruby
Requires: rubygem-ffi >= 1.9.0

%description
Provides the ability to navigate and read entries from the systemd journal in ruby,
as well as write events to the journal.

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.1.0-1.1.1
- Adjusted to build for subrelease 90
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.1.0-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.1.0-1
- Upgrade to 2.1.0
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.2-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.2-2
- Release bump for SRP compliance
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.2-1
- Automatic Version Bump
* Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.3.3-1
- Initial build
