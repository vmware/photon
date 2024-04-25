%global debug_package %{nil}
%global gem_name msgpack

Name: rubygem-msgpack
Version:        1.3.3
Release:        3%{?dist}
Summary:        A binary-based efficient object serialization library
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/msgpack-%{version}.gem
%define sha512  msgpack=18d78cac70a14a22fab6f7743f702cbb1a636434e881dff5b6eec89be137a47fac1649e143dfa8c3c9e65ccc099b2b3c778cb333613d750cb6b296e3ce7db3c9

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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.3-3
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.3-2
-   Build from source
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.3-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.4-1
-   Initial build
