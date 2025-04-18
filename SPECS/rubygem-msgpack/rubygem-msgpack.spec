%global debug_package %{nil}
%global gem_name msgpack

Name: rubygem-msgpack
Version:        1.7.2
Release:        3%{?dist}
Summary:        A binary-based efficient object serialization library
Group:          Development/Languages
Distribution:   Photon
Vendor:         VMware, Inc.
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/msgpack-%{version}.gem
%define sha512 %{gem_name}=1ff8027f39971729e0af3a293a7ddc56e06ac6a5dd4aeb444b4f0e0ac0a9dfb5ab99e6cdbd4077655c5d17406b2a895c27ebdd310ff8d298ad7ea4601d2bc2c9

Source1: license.txt
%include %{SOURCE1}

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
*   Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.2-3
-   Build gems properly
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.2-2
-   Add gem macros
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.2-1
-   Update to version 1.7.2
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.3-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.4-1
-   Initial build
