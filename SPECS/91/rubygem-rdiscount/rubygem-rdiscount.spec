%global build_if %{photon_subrelease} <= 91
%global debug_package %{nil}
%global gem_name rdiscount

Name: rubygem-rdiscount
Version:        2.2.7.3
Release:        1.2%{?dist}
Summary:        Fast Implementation of Gruber's Markdown in C
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel
Requires:       ruby

Patch0:         CVE-2026-35201.patch

%description
RDiscount converts documents in Markdown syntax to HTML.
It uses the excellent Discount processor by David Loren Parsons for this purpose,
and thereby inherits Discount’s numerous useful extensions to the Markdown language.

%prep
%gem_unpack %{SOURCE0}
%autopatch -p1

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
* Thu Apr 09 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7.3-1.2
- Fix CVE-2026-35201
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7.3-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7.3-1
- Upgrade to 2.2.7.3
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7-4
- Release bump for SRP compliance
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7-3
- Add gem macros
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7-2
- Build from source
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.7-1
- Automatic Version Bump
* Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.2.0.2-1
- Initial build
