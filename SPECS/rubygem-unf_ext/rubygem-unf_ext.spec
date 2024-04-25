%global debug_package %{nil}
%global gem_name unf_ext

Name: rubygem-unf_ext
Version:        0.0.7.7
Release:        3%{?dist}
Summary:        Unicode Normalization Form support library for CRuby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  unf_ext=7dc75f071be4d4f3cd44f64a26c5f63f01494f79f3585eea3b307c3e8133b17b1007c4b36915f7254e516ae7a62268be8f3e4b250dcec7a9a083b5a66582887d
BuildRequires:  ruby
BuildRequires:  ruby-devel
BuildRequires:  gmp-devel

%description
Unicode Normalization Form support library for CRuby.

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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.7.7-3
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.7.7-2
-   Build from source
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.0.7.7-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-2
-   Enabled build for non x86_64 build archs
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-1
-   Initial build
