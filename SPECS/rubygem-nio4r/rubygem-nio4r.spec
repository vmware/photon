%global debug_package %{nil}
%global gem_name nio4r

Name: rubygem-nio4r
Version:        2.5.8
Release:        4%{?dist}
Summary:        Cross-platform asynchronous I/O primitives for scalable network clients and servers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  nio4r=3942403147882380b86f42c54a6d4e92c4e85dd3c0b5b9f473a05fcf98c041853e21d11d0481d1973342b5a4bfb59e02cfd523a44e9e45c3740627a45f7f99c7

Source1: license.txt
%include %{SOURCE1}
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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.8-4
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.8-3
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.8-2
-   Build from source
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.5.8-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.4-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.2-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-2
-   Enabled build for non x86_64 build archs
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-1
-   Initial build
