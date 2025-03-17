%global debug_package %{nil}
%global gem_name unf_ext

Name: rubygem-unf_ext
Version:        0.0.8.2
Release:        4%{?dist}
Summary:        Unicode Normalization Form support library for CRuby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby-devel
BuildRequires:  gmp-devel
Requires:       ruby

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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.8.2-4
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.8.2-3
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.8.2-2
-   Build from source
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.0.8.2-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.0.7.7-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-2
-   Enabled build for non x86_64 build archs
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-1
-   Initial build
