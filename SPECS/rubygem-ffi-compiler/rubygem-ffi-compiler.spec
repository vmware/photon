%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ffi-compiler

Name:           rubygem-ffi-compiler
Version:        1.0.1
Release:        1%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=7a13625ab1c5748d05ec93d68708dd9435ec92dcd0c823109c44173fdaf8710aec5f5b4fb11966475f10ae91401c7ca3c620f9d36bb9ca665114e1ed70f4edd0

BuildRequires: ruby

Requires: rubygem-ffi
Requires: ruby

BuildArch: noarch

%description
An easy-to-use client library for making requests from Ruby. It uses a simple
method chaining system for building requests, similar to Python's Requests.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-1
- Initial version.
- Needed by rubygem-http-parser.
