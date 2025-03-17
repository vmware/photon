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
