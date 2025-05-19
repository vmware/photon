%global debug_package %{nil}
%global gem_name kubeclient

Name:           rubygem-kubeclient
Version:        4.9.3
Release:        1%{?dist}
Summary:        A client for Kubernetes REST api.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  kubeclient=f31a516fc55231ac65f02a0a49627819c3bcde08860af5d4695702ebe4ccba1fd3d31f199cdf3f4389b36e8f257a8ab5c8b73c045b3ff31d7dc381e4ede9d94f

BuildArch: noarch

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
*   Mon May 19 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.9.3-1
-   Upgrade to 4.9.3 to fix CVE-2022-0759
*   Wed Mar 05 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.9.1-7
-   Set buildarch to noarch
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
