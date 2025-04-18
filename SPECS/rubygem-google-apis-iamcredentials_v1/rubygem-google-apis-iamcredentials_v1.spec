%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-apis-iamcredentials_v1

Summary:        This is a simple REST client for IAM Service Account Credentials API V1.
Name:           rubygem-google-apis-iamcredentials_v1
Version:        0.22.0
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=7266820dc9655ed636e8aa8fe5191ab62cbbb53cafce9290c6df053994047543fe8e65d41ae17cbf464915a4067505a9b549297e12a2491c740c31aa1ac1afe4

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-google-apis-core

Requires: ruby
Requires: rubygem-google-apis-core

%description
This is a simple REST client for IAM Service Account Credentials API V1.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.22.0-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.22.0-1
- Initial version.
