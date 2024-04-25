%global debug_package %{nil}
%global gem_name rdiscount

Name: rubygem-rdiscount
Version:        2.2.7.3
Release:        2%{?dist}
Summary:        Fast Implementation of Gruber's Markdown in C
Group:          Development/Languages
License:        BSD-3-CLAUSE
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  rdiscount=525791f2be10e118f556676a1645d2805ba6ad920e4f4c8761362c5aa09cf1f773f0216f7b6c2e1f78acbc1de1ac85c6088cc85729af70a28f537fdff3434786
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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7.3-2
-   Add gem macros
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7.3-1
-   Update to version 2.2.7.3
*   Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.7-1
-   Automatic Version Bump
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.2.0.2-1
-   Initial build
