%global debug_package %{nil}
%global gem_name oj

Name: rubygem-oj
Version:        3.13.21
Release:        4%{?dist}
Summary:        The fastest JSON parser and object serializer.
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
The fastest JSON parser and object serializer.

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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.13.21-4
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.13.21-3
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.13.21-2
-   Build from source
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.13.21-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.10.14-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.10.13-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.3.10-2
-   Enabled build for non x86_64 build archs
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.3.10-1
-   Initial build
