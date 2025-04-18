%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ffi-compiler

Name:           rubygem-ffi-compiler
Version:        1.0.1
Release:        3%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=7a13625ab1c5748d05ec93d68708dd9435ec92dcd0c823109c44173fdaf8710aec5f5b4fb11966475f10ae91401c7ca3c620f9d36bb9ca665114e1ed70f4edd0

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-ffi

Requires: rubygem-ffi
Requires: ruby

BuildArch: noarch

%description
An easy-to-use client library for making requests from Ruby. It uses a simple
method chaining system for building requests, similar to Python's Requests.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0.1-3
- Build gems properly
* Tue Mar 05 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.1-2
- Bump version with rubygem-ffi upgrade
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-1
- Initial version.
- Needed by rubygem-http-parser.
