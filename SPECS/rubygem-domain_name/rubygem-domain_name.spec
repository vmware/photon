%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name domain_name

Name: rubygem-domain_name
Version:        0.5.20190701
Release:        3%{?dist}
Summary:        This is a Domain Name manipulation library for Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  domain_name=445f0e8a377bb700f8a3b926970f4351d28759e237947d6c755afff52726141c6b821b43b2a761d4d0d6237969304ef749404a5f383f69710b04803410dc70aa

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

Requires: rubygem-unf >= 0.0.5, rubygem-unf < 1.0.0
BuildArch: noarch

%description
This is a Domain Name manipulation library for Ruby. It can also be used for
cookie domain validation based on the Public Suffix List.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.5.20190701-3
-   Release bump for SRP compliance
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.5.20190701-2
-   Rebuilt using ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.5.20190701-1
-   Initial build
