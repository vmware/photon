%global debug_package %{nil}
%global gem_name bundler

Name:           rubygem-bundler
Version:        2.2.33
Release:        3%{?dist}
Summary:        manages an application's dependencies
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/bundler-%{version}.gem
%define sha512 bundler=8ac6bc00eb7a206fbd4e0d0de5d636583f48006b51352e50896230afba1098aeae2418694c8592f73af02612fe8e10dacd71b79804b724fad7633b23c81f1d14

BuildRequires:  ruby-devel
BuildRequires:  findutils

%description
Bundler manages an application's dependencies through its entire life
across many machines, systematically and repeatably.

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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.33-3
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.33-2
-   Build from source
*   Wed Dec 15 2021 Piyush Gupta <gpiyush@vmware.com> 2.2.33-1
-   Upgrade to 2.2.33.
*   Mon Nov 01 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.2.21-2
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Thu Jul 08 2021 Piyush Gupta <gpiyush@vmware.com> 2.2.21-1
-   Upgrade to 2.2.21, Fixes CVE-2020-36327, CVE-2019-3881.
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.4-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.16.4-1
-   Update to version 1.16.4
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.16.3-1
-   Initial build
