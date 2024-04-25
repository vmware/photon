%global debug_package %{nil}
%global gem_name oj

Name: rubygem-oj
Version:        3.10.14
Release:        3%{?dist}
Summary:        The fastest JSON parser and object serializer.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  oj=b1b273bd3dcf4cdf47292dae6a7cdd15887051ad242326f884468ee8a3abbbd2f7da654069ce620190464e46979650617283e5a2568c322ac83d253f3c6bf9a9
BuildRequires:  ruby-devel
BuildRequires:  gmp-devel

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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.10.14-3
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.10.14-2
-   Build from source
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.10.14-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.10.13-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.3.10-2
-   Enabled build for non x86_64 build archs
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.3.10-1
-   Initial build
