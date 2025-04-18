%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name jwt

Summary:        A pure ruby implementation of the RFC 7519 OAuth JSON Web Token (JWT) standard.
Name:           rubygem-jwt
Version:        2.10.1
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=5b61b2049df5930a66ee69df221ff7b2d2ef71a18c6cac65e6c1c6f0434a220364a54a607464665bd2c5e4572309dc22832ee1fa30f78c70371fe0d1ce991698

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
A pure ruby implementation of the RFC 7519 OAuth JSON Web Token (JWT) standard.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.10.1-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.10.1-1
- Initial version.
