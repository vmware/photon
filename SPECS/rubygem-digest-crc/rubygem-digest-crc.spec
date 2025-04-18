%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name digest-crc

Summary:        Adds support for calculating Cyclic Redundancy Check (CRC) to the Digest module.
Name:           rubygem-digest-crc
Version:        0.7.0
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=5057385de6c548bf4a78bee6dbeb9ae74b270af7786d18615a31dc30e3fc0351cbf4103c7d5714e0b09d352158c3589fd757fb03ade0a15b4e95bfdea08f323f

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Adds support for calculating Cyclic Redundancy Check (CRC) to the Digest module.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.7.0-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.7.0-1
- Initial version.
