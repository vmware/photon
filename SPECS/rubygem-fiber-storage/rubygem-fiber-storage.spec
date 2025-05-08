%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fiber-storage

Summary:        Ruby Gem for Fiber Storage.
Name:           rubygem-fiber-storage
Version:        1.0.1
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch: noarch

%description
Fiber Storage is a Ruby gem designed for storage management using fibers, providing an asynchronous and efficient way to manage resources.

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
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.1-1
- Initial version
