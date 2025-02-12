%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mini_mime

Summary:        A minimal mime type library.
Name:           rubygem-mini_mime
Version:        1.1.5
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=036d657910f34385f23fd78110716ee01f2139847fac8fb06a4f505285dea1f1024e2adc4c4895f2c1248047bf9c333bbae3decb9d5351816a79d69ebf7a15c2

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Minimal mime type implementation for use with the mail and rest-client gem.

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.5-1
- Initial version.
