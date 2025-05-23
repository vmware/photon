%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-cloud-errors

Summary:        google-cloud-errors defines error classes for google-cloud-ruby.
Name:           rubygem-google-cloud-errors
Version:        1.4.0
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=3c12e59795abc2e3aee62b463fa7ab70deca6b5cecaa919b925bcb03ed7a1e67455e40a5bfb9c1380aae16d5a5e9bd9a125d0ef8d346aa54c07545dc32b8a042

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
google-cloud-errors defines error classes for google-cloud-ruby.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.0-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.0-1
- Initial version.
