%global build_if %{photon_subrelease} >= 92
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name connection_pool

Name: rubygem-connection_pool
Version:        3.0.2
Release:        1%{?dist}
Summary:        Generic connection pool for Ruby
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/connection_pool/versions/%{version}
Source0:        https://rubygems.org/downloads/connection_pool-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Generic connection pool for Ruby.
Provides a thread-safe connection pooling mechanism for any type of connection.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Jan 27 2026 Mukul Sikka <mukul.sikka@broadcom.com> 3.0.2-1
- Initial build for activesupport dependency
