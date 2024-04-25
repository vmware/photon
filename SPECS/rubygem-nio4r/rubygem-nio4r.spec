%global debug_package %{nil}
%global gem_name nio4r

Name: rubygem-nio4r
Version:        2.5.4
Release:        3%{?dist}
Summary:        Cross-platform asynchronous I/O primitives for scalable network clients and servers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  nio4r=f7e383516ac6b55fd49339280e624a4c35f9cd2d31915b3d117189506522d967fc53a43cde75e8601f3fe0530e1322aeaa8c94a09289ddbefb2afd8d067341ec
BuildRequires:  gmp-devel
BuildRequires:  ruby-devel
Requires:       ruby

%description
Cross-platform asynchronous I/O primitives for scalable network clients and servers.
Inspired by the Java NIO API, but simplified for ease-of-use.

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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.4-3
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.4-2
-   Build from source
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.4-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.2-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-2
-   Enabled build for non x86_64 build archs
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-1
-   Initial build
