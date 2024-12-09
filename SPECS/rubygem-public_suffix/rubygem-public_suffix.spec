%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name public_suffix

Name: rubygem-public_suffix
Version:        5.0.0
Release:        2%{?dist}
Summary:        PublicSuffix can parse and decompose a domain name into top level domain, domain and subdomains.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512    public_suffix=89dc076e6c55790b1459ceb0b0587d20b80d8a681bab6db2dd213e06f9bf9e55200e86cf891c92b310e691e7b0e1bb5ae95e28e3a3307541c2f020e5f69abeb5

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby >= 2.1.0

BuildArch: noarch

%description
PublicSuffix can parse and decompose a domain name into top level domain, domain and subdomains.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.0.0-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 5.0.0-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.6-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 3.1.1-2
-   Built with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.1.1-1
-   Initial build
