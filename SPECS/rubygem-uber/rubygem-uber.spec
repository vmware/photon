%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name uber

Summary:        A gem-authoring framework.
Name:           rubygem-uber
Version:        0.1.0
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=92b374b265ac4fac861db3aa07ca1f2c688f74e55434ebf2088b60e6220a46c0a9405792d6d483015677fe0c4430dfdd8809b2620b430afb667fc0a5a499502b

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Gem-authoring extensions for classes and modules.

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.1.0-1
- Initial version.
