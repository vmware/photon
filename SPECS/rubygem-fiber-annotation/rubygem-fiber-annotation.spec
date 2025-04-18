%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fiber-annotation

Name:           rubygem-fiber-annotation
Version:        0.2.0
Release:        2%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=4a0d51c753e1c6ad47881302c643821892a5f544aa8a73b64555a0d545c8c9780ef3af88580dbb8452732cae6c6ba24406cd41e87a256c4b2f9f4077357cfbbe

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch: noarch

%description
Provides low level cross-platform primitives for constructing
event loops, with support for select, kqueue, epoll and io_uring.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.2.0-2
- Build gems properly
* Wed Apr 10 2024 Shivani Agarwal <shivani.agarwal@braodcom.com> 0.2.0-1
- Initial version. Needed by rubygem-async-http packages.
