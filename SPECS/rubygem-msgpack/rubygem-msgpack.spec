%global debug_package %{nil}
%global gem_name msgpack

Name: rubygem-msgpack
Version:        1.6.0
Release:        4%{?dist}
Summary:        A binary-based efficient object serialization library
Group:          Development/Languages
Distribution:   Photon
Vendor:         VMware, Inc.
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/msgpack-%{version}.gem

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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.6.0-4
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.6.0-3
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.6.0-2
-   Build from source
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.3-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.4-1
-   Initial build
