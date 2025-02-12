%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name trailblazer-option

Summary:        A powerful set of gems that simplifies the implementation of clean Ruby applications.
Name:           rubygem-trailblazer-option
Version:        0.1.2
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=427cfdceafcecdb2d746320b8bb3f185f230be47a52dde2358b85de3674c8280e8d92fd5a75ac6421e010ec3b4f401bd0e8e71ebd66c2fcf6d4ca043daede0a3

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Trailblazer is a collection of gems to help you structure growing Ruby applications.
It does so by providing a higher level of architecture through new abstractions.

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.1.2-1
- Initial version.
