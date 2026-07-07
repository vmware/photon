%global debug_package %{nil}
%global gem_name oj

Name: rubygem-oj
Version:        3.17.3
Release:        1%{?dist}
Summary:        The fastest JSON parser and object serializer.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  oj=af5c77c1ab17a5c5fa2f0c6fed174c2c13d447df3b14ef2a5fd27fb2222393ab835b7fe2aa3f98ed59d0957c587ad197edc15e7acffc098dc192bede6d766485

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
*   Tue Jul 07 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.17.3-1
-   Fix CVE-2026-54592, CVE-2026-54903, CVE-2026-54902, CVE-2026-54901, CVE-2026-54900
-   CVE-2026-54899, CVE-2026-54898, CVE-2026-54897, CVE-2026-54896, CVE-2026-54502
-   CVE-2026-54500
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
