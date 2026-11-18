%global debug_package %{nil}
%global gem_name msgpack

Name: rubygem-msgpack
Version:        1.8.7
Release:        1%{?dist}
Summary:        A binary-based efficient object serialization library
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/msgpack-%{version}.gem
%define sha512  msgpack=88a8e3338015db2d4572829d61fb30906829bb78c888853931ee34f19630f2fcd41b61713b5cae6041e74c0ebb08ee8b4fb808f4a3acef8599ef64d61e10cf07

BuildRequires:  ruby-devel

Requires:       ruby

%description
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like JSON.
But unlike JSON, it is very fast and small.

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
*   Wed Nov 18 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.8.7-1
-   Upgrade to v1.8.7 to fix CVE-2026-126366
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.3-3
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.3-2
-   Build from source
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.3-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.4-1
-   Initial build
