%global debug_package %{nil}
%global gem_name kubeclient

Name:           rubygem-kubeclient
Version:        4.9.1
Release:        6%{?dist}
Summary:        A client for Kubernetes REST api.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  kubeclient=bc4ea2ae7dac142afec5d4de171f58871ea87aa2205c5d96ebbf3966377a4c4d4099b400bc958ee34f7983760fcff8197c73ca18fb1b452cf65f68ea0b0758a0

BuildRequires:  ruby-devel
BuildRequires:  rubygem-activesupport
BuildRequires:  rubygem-http
BuildRequires:  rubygem-recursive-open-struct
BuildRequires:  rubygem-jsonpath
BuildRequires:  rubygem-rest-client
BuildRequires:  findutils
BuildRequires:  rubygem-http-accept

Requires:       rubygem-activesupport
Requires:       rubygem-http >= 3.0, rubygem-http < 5.0
Requires:       rubygem-recursive-open-struct > 1.1
Requires:       rubygem-rest-client
Requires:       rubygem-http-accept >= 1.7.0, rubygem-http-accept < 2.0
Requires:       rubygem-jsonpath
Requires:       ruby

%description
A client for Kubernetes REST api.

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
*   Thu Feb 27 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.9.1-6
-   Bump version with rubygem-activesupport bump
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.9.1-5
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.9.1-4
-   Build from source
*   Mon Jan 08 2024 Shivani Agarwal <shivania2@vmware.com> 4.9.1-3
-   Fix requires
*   Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.9.1-2
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.9.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.1.4-2
-   Rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.4-1
-   Initial build
