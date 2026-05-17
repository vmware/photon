%global build_if %{photon_subrelease} <= 90
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name io-endpoint

Summary:        Abstraction for IO endpoints including sockets, SSL, pipes, etc.
Name:           rubygem-io-endpoint
Version:        0.15.2
Release:        1.1.1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch:      noarch

%description
`io-endpoint` provides a unified abstraction for different IO sources in Ruby,
including TCP, SSL, pipes, and more. It simplifies working with asynchronous
and synchronous IO in Ruby applications.

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.15.2-1.1.1
- Adjusted to build for subrelease 90
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.15.2-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.15.2-1
- Initial version.
