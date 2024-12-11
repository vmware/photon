%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name addressable

Name: rubygem-addressable
Version:        2.8.1
Release:        2%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512    addressable=ae0b7cb5fdc0b5b8717637e9589ab9167aa3924253f4c9102134b1e5aee07c7f5e3e92e2e32ca872b4a72a3a70c8086c7073cbbddf7cbb6e1948ed97de2c9108

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby >= 2.0.0
Requires: rubygem-public_suffix >= 2.0.2, rubygem-public_suffix < 5.0.1
BuildArch: noarch

%description
Addressable is a replacement for the URI implementation that is part of Ruby's standard library.
It more closely conforms to the relevant RFCs and adds support for IRIs and URI templates.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.8.1-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.8.1-1
-   Automatic Version Bump
*   Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-2
-   Update rubygem-public_suffix version
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-1
-   Automatic Version Bump
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.6.0-1
-   Initial build
