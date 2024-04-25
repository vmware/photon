%global debug_package %{nil}
%global gem_name rdiscount

Name: rubygem-rdiscount
Version:        2.2.0.2
Release:        3%{?dist}
Summary:        Fast Implementation of Gruber's Markdown in C
Group:          Development/Languages
License:        BSD-3-CLAUSE
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  rdiscount=97a0fabb77238173f101298e4b4b6d4728b9e15cb7d3f14e7d1d978c44ab92dd89c2e02d0c15c0fa70a836eb54abca06b0027e26e5d87540bfe145c8527be3f7
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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.0.2-3
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.0.2-2
-   Build from source
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.2.0.2-1
-   Initial build
