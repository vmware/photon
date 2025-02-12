%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-apis-core

Summary:        Common utility and base classes for legacy Google REST clients
Name:           rubygem-google-apis-core
Version:        0.16.0
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=9cd658a8e5fb40485de18a588a72643e3258a9b0b9cff8e96060e431faefd6df34aae9b6c473b59765d07d953385e2914c9048801909523a38bf8c91da975c92

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-httpclient
BuildRequires: rubygem-googleauth
BuildRequires: rubygem-mini_mime
BuildRequires: rubygem-retriable
BuildRequires: rubygem-representable

Requires: ruby
Requires: rubygem-representable
Requires: rubygem-mini_mime
Requires: rubygem-retriable
Requires: rubygem-addressable
Requires: rubygem-googleauth
Requires: rubygem-httpclient

%description
Common utility and base classes for legacy Google REST clients

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.16.0-1
- Initial version.
