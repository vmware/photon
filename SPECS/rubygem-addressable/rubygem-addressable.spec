%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name addressable

Name: rubygem-addressable
Version:        2.7.0
Release:        3%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512    addressable=4c438bbfa8874fdcf11eef1d1f7cceb1855ea85948daff13615a0af129d35f92cc918f4bd5bbe4cd6ebccc67a86fc582265f915dc39831ec64209de0bdeeb732

BuildRequires:  ruby >= 2.0.0
BuildRequires:  ruby-devel

Requires: rubygem-public_suffix >= 2.0.2, rubygem-public_suffix < 5.0
BuildArch: noarch

Patch0: CVE-2026-35611-1.patch
Patch1: CVE-2026-35611-2.patch
Patch2: CVE-2026-35611-3.patch

%description
Addressable is a replacement for the URI implementation that is part of Ruby's standard library.
It more closely conforms to the relevant RFCs and adds support for IRIs and URI templates.

%prep
%gem_unpack %{SOURCE0}
%autopatch -p1

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Apr 21 2026 Mukul Sikka <mukul.sikka@broadcom.com> 2.7.0-3
- Fix CVE-2026-35611
* Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-2
- Update rubygem-public_suffix version
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-1
- Automatic Version Bump
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.6.0-1
- Initial build
