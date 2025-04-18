%global debug_package %{nil}
%global gem_name rdiscount

Name: rubygem-rdiscount
Version:        2.2.7
Release:        4%{?dist}
Summary:        Fast Implementation of Gruber's Markdown in C
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ruby-devel
Requires:       ruby

%description
RDiscount converts documents in Markdown syntax to HTML.
It uses the excellent Discount processor by David Loren Parsons for this purpose,
and thereby inherits Discount’s numerous useful extensions to the Markdown language.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
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
