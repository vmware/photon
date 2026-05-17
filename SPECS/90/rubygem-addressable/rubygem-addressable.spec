%global build_if %{photon_subrelease} <= 90
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name addressable

Name: rubygem-addressable
Version:        2.8.7
Release:        1.2.1%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

Patch0:         CVE-2026-35611-1.patch
Patch1:         CVE-2026-35611-2.patch
Patch2:         CVE-2026-35611-3.patch

BuildArch: noarch

BuildRequires: ruby-devel
BuildRequires: rubygem-public_suffix

Requires: rubygem-public_suffix >= 2.0.2, rubygem-public_suffix < 6.0.3
Requires: ruby

%description
Addressable is a replacement for the URI implementation that is part of Ruby's standard library.
It more closely conforms to the relevant RFCs and adds support for IRIs and URI templates.

%prep
%gem_unpack %{SOURCE0}
%autopatch -p1

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.8.7-1.2.1
- Adjusted to build for subrelease 90
* Wed Apr 22 2026 Mukul Sikka <mukul.sikka@broadcom.com> 2.8.7-1.2
- Fix CVE-2026-35611
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.8.7-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.8.7-1
- Upgrade to 2.8.7
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.8.1-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.8.1-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.8.1-1
- Automatic Version Bump
* Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-2
- Update rubygem-public_suffix version
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-1
- Automatic Version Bump
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.6.0-1
- Initial build
